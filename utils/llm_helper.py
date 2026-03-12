
"""LLM integration helper with ChromaDB RAG for career intelligence analysis."""

import os
import re
import uuid
import logging
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
import chromadb

load_dotenv()

logger = logging.getLogger(__name__)


class RAGVectorStore:
    """ChromaDB-backed vector store for resume and job posting chunks.
    
    Embeddings are generated manually via the OpenAI API (openai>=1.0.0 compatible)
    and passed directly to ChromaDB — no ChromaDB embedding function wrapper used.
    """

    EMBED_MODEL = "text-embedding-ada-002"

    def __init__(self, openai_api_key: str):
        self._openai = OpenAI(api_key=openai_api_key)
        self.client = chromadb.Client()
        self._collections: Dict[str, chromadb.Collection] = {}

    def _embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using the new openai>=1.0.0 API."""
        texts = [t.replace("\n", " ") for t in texts]
        response = self._openai.embeddings.create(input=texts, model=self.EMBED_MODEL)
        return [item.embedding for item in response.data]

    def _safe_name(self, name: str) -> str:
        """Convert any string to a valid ChromaDB collection name."""
        clean = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        safe = f"col_{clean}"[:63]
        return safe if len(safe) >= 3 else f"{safe}_x"

    def _get_or_create_collection(self, name: str) -> chromadb.Collection:
        """Get or create a named ChromaDB collection (no embedding_function)."""
        safe_name = self._safe_name(name)
        if safe_name not in self._collections:
            # Do NOT pass embedding_function — we handle embeddings manually
            self._collections[safe_name] = self.client.get_or_create_collection(
                name=safe_name
            )
        return self._collections[safe_name]

    def index_document(self, text_chunks: List[str], doc_id: str, doc_type: str) -> bool:
        """Index document chunks into ChromaDB.

        Args:
            text_chunks: List of text chunks from the document
            doc_id: Unique identifier for the document (e.g., 'resume' or 'job_1')
            doc_type: Type label ('resume' or 'job')

        Returns:
            True on success, False on failure
        """
        try:
            collection = self._get_or_create_collection(doc_id)

            # Clear existing docs before re-indexing
            existing = collection.get()
            if existing["ids"]:
                collection.delete(ids=existing["ids"])

            ids = [str(uuid.uuid4()) for _ in text_chunks]
            metadatas = [
                {"doc_id": doc_id, "doc_type": doc_type, "chunk_index": i}
                for i, _ in enumerate(text_chunks)
            ]
            embeddings = self._embed(text_chunks)
            collection.add(documents=text_chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
            logger.info(f"Indexed {len(text_chunks)} chunks for doc_id='{doc_id}'")
            return True
        except Exception as e:
            logger.error(f"ERROR during indexing doc_id='{doc_id}': {str(e)}")
            print(f"ERROR during indexing doc_id='{doc_id}': {str(e)}")
            return False

    def retrieve(self, doc_id: str, query: str, k: int = 4) -> str:
        """Retrieve top-k relevant chunks from a document collection.

        Args:
            doc_id: Document identifier to query against
            query: User query string
            k: Number of top chunks to retrieve

        Returns:
            Concatenated relevant context string
        """
        try:
            safe_name = self._safe_name(doc_id)
            if safe_name not in self._collections:
                return ""
            collection = self._collections[safe_name]
            count = collection.count()
            if count == 0:
                return ""
            query_embedding = self._embed([query])[0]
            results = collection.query(query_embeddings=[query_embedding], n_results=min(k, count))
            docs = results.get("documents", [[]])[0]
            return "\n\n".join(docs)
        except Exception as e:
            logger.error(f"ERROR during retrieval doc_id='{doc_id}': {str(e)}")
            return ""

    def delete_document(self, doc_id: str):
        """Remove a document collection."""
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', doc_id)
        safe_name = f"col_{clean_name}"[:63]
        if safe_name in self._collections:
            self.client.delete_collection(safe_name)
            del self._collections[safe_name]

    def reset(self):
        """Clear all collections."""
        for name in list(self._collections.keys()):
            try:
                self.client.delete_collection(name)
            except Exception:
                pass
        self._collections.clear()


class CareerIntelligenceAssistant:
    """LLM-powered career intelligence assistant with ChromaDB RAG."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY in .env or pass it directly."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"
        self.rag = RAGVectorStore(openai_api_key=self.api_key)

    # ── Indexing ──────────────────────────────────────────────────────────────

    def index_resume(self, chunks: List[str]) -> bool:
        """Index resume chunks into ChromaDB. Returns True on success."""
        return self.rag.index_document(chunks, doc_id="resume", doc_type="resume")

    def index_job(self, chunks: List[str], job_num: int, job_name: str) -> bool:
        """Index a job posting's chunks into ChromaDB. Returns True on success."""
        doc_id = f"job_{job_num}"
        return self.rag.index_document(chunks, doc_id=doc_id, doc_type="job")

    def remove_job(self, job_num: int):
        """Remove a job posting from the vector store."""
        self.rag.delete_document(f"job_{job_num}")

    def reset_store(self):
        """Clear all indexed documents."""
        self.rag.reset()

    # ── RAG retrieval ─────────────────────────────────────────────────────────

    def _build_rag_context(
        self,
        query: str,
        job_postings: Dict[int, Dict[str, str]],
        k: int = 4
    ) -> str:
        """Retrieve relevant chunks from resume + all job postings for a query."""
        context_parts = []

        resume_ctx = self.rag.retrieve("resume", query, k=k)
        if resume_ctx:
            context_parts.append(f"=== RELEVANT RESUME SECTIONS ===\n{resume_ctx}")

        for job_num, job_data in job_postings.items():
            job_ctx = self.rag.retrieve(f"job_{job_num}", query, k=k)
            if job_ctx:
                context_parts.append(
                    f"=== RELEVANT SECTIONS — Job #{job_num}: {job_data['name']} ===\n{job_ctx}"
                )

        return "\n\n".join(context_parts)

    # ── LLM calls ─────────────────────────────────────────────────────────────

    def get_response(
        self,
        resume: str,
        job_postings: Dict[int, Dict[str, str]],
        conversation_history: List[Dict[str, str]],
        user_message: str
    ) -> str:
        """Get RAG-augmented LLM response."""
        rag_context = self._build_rag_context(user_message, job_postings)

        system_prompt = f"""You are a Career Intelligence Assistant — an expert career advisor and recruiter.
You have access to the candidate's resume and job postings, retrieved via semantic search.

{rag_context}

Guidelines:
1. Reference specific skills, experience, and requirements from the retrieved context above.
2. Use "Job #N" format when referring to specific job postings.
3. Provide actionable, honest, and encouraging advice.
4. For skill gaps, suggest concrete learning resources or steps.
5. For interview prep, suggest likely questions and talking points.
6. Consider both hard skills (technical) and soft skills."""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting response: {str(e)}. Please check your API key."

    def get_quick_analysis(self, job_num: int, job_name: str) -> str:
        """Get a quick fit analysis for a specific job using RAG."""
        query = f"skills experience qualifications requirements fit for {job_name}"

        resume_ctx = self.rag.retrieve("resume", query, k=5)
        job_ctx = self.rag.retrieve(f"job_{job_num}", query, k=5)

        prompt = f"""Analyze the candidate's fit for: {job_name}

=== CANDIDATE RESUME (relevant sections) ===
{resume_ctx}

=== JOB REQUIREMENTS (relevant sections) ===
{job_ctx}

Provide a concise analysis:
1. Overall Fit Score (0–100%)
2. Top 3 Matching Strengths
3. Top 3 Skill Gaps
4. Key Recommendations

Be specific and reference actual content from the sections above."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a career intelligence assistant providing concise, specific analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting analysis: {str(e)}"