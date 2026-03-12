

"""
Career Intelligence Assistant - Streamlit Application
RAG-powered (ChromaDB) career fit assessment and interview preparation.
"""

import streamlit as st
import os
from typing import Dict, List
from dotenv import load_dotenv

# Load .env from project root
load_dotenv()

from utils.document_parser import DocumentParser
from utils.llm_helper import CareerIntelligenceAssistant


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career Intelligence Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size:2.5rem; font-weight:bold; color:#1E88E5; text-align:center; padding:1rem 0; }
    .sub-header  { font-size:1.2rem; color:#666; text-align:center; margin-bottom:2rem; }
    .chat-message { padding:1rem; border-radius:0.5rem; margin:0.5rem 0; }
    .user-message      { background-color:#e3f2fd; }
    .assistant-message { background-color:#f5f5f5; }
    .stButton>button { width:100%; }
    .rag-badge { background:#e8f5e9; color:#2e7d32; padding:2px 8px;
                 border-radius:12px; font-size:0.75rem; font-weight:600; }
    </style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
def initialize_session_state():
    defaults = {
        'resume_text': None,
        'resume_filename': None,
        'resume_indexed': False,
        'job_postings': {},       # {job_num: {"name": str, "content": str, "indexed": bool}}
        'conversation_history': [],
        'assistant': None,
        'job_counter': 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # Try to init assistant from .env key on first load
    if st.session_state.assistant is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
            except Exception:
                st.session_state.assistant = None


# ── Helpers ────────────────────────────────────────────────────────────────────
def parse_and_index_resume(uploaded_file) -> bool:
    """Parse resume, chunk it, and index into ChromaDB."""
    try:
        file_bytes = uploaded_file.read()
        text = DocumentParser.parse_file(file_bytes, uploaded_file.name)
        chunks = DocumentParser.chunk_text(text)

        st.session_state.resume_text = text
        st.session_state.resume_filename = uploaded_file.name
        st.session_state.resume_indexed = False

        if st.session_state.assistant:
            st.session_state.assistant.index_resume(chunks)
            st.session_state.resume_indexed = True

        return True
    except Exception as e:
        st.error(f"Error parsing resume: {str(e)}")
        return False


def parse_and_index_job(uploaded_file) -> bool:
    """Parse a job posting, chunk it, and index into ChromaDB."""
    try:
        file_bytes = uploaded_file.read()
        text = DocumentParser.parse_file(file_bytes, uploaded_file.name)
        chunks = DocumentParser.chunk_text(text)

        st.session_state.job_counter += 1
        job_num = st.session_state.job_counter
        indexed = False

        if st.session_state.assistant:
            st.session_state.assistant.index_job(chunks, job_num, uploaded_file.name)
            indexed = True

        st.session_state.job_postings[job_num] = {
            "name": uploaded_file.name,
            "content": text,
            "indexed": indexed,
            "chunks": len(chunks),
        }
        return True
    except Exception as e:
        st.error(f"Error parsing {uploaded_file.name}: {str(e)}")
        return False


def reindex_all():
    """Re-index all documents after API key is set."""
    assistant = st.session_state.assistant
    if not assistant:
        return

    # Re-index resume
    if st.session_state.resume_text and not st.session_state.resume_indexed:
        chunks = DocumentParser.chunk_text(st.session_state.resume_text)
        assistant.index_resume(chunks)
        st.session_state.resume_indexed = True

    # Re-index jobs
    for job_num, job_data in st.session_state.job_postings.items():
        if not job_data.get("indexed"):
            chunks = DocumentParser.chunk_text(job_data["content"])
            assistant.index_job(chunks, job_num, job_data["name"])
            st.session_state.job_postings[job_num]["indexed"] = True


def handle_user_message(user_message: str):
    if not st.session_state.resume_text:
        st.error("⚠️ Please upload your resume first!")
        return
    if not st.session_state.assistant:
        st.error("⚠️ Please configure your OpenAI API key!")
        return

    st.session_state.conversation_history.append({"role": "user", "content": user_message})

    with st.spinner("🔍 Retrieving relevant context & generating response..."):
        response = st.session_state.assistant.get_response(
            resume=st.session_state.resume_text,
            job_postings=st.session_state.job_postings,
            conversation_history=st.session_state.conversation_history[:-1],
            user_message=user_message
        )

    st.session_state.conversation_history.append({"role": "assistant", "content": response})
    st.rerun()


# ── Sidebar ────────────────────────────────────────────────────────────────────
def sidebar_config():
    st.sidebar.markdown("## 🎯 Career Intelligence Assistant")
    st.sidebar.markdown('<span class="rag-badge">⚡ RAG · ChromaDB</span>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

    # API Key
    st.sidebar.markdown("### 🔑 API Configuration")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        value=os.getenv('OPENAI_API_KEY', ''),
        type="password",
        help="Reads from .env automatically if set"
    )

    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        if not st.session_state.assistant:
            try:
                st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
                reindex_all()   # index any docs uploaded before key was set
                st.sidebar.success("✅ API key configured!")
            except Exception as e:
                st.sidebar.error(f"❌ {str(e)}")
        else:
            st.sidebar.success("✅ API key active")
    else:
        st.sidebar.warning("⚠️ API key required for AI features")

    st.sidebar.markdown("---")

    # Resume upload
    st.sidebar.markdown("### 📄 Upload Resume")
    resume_file = st.sidebar.file_uploader(
        "Upload your resume", type=['pdf', 'docx', 'txt'], key="resume_uploader"
    )
    if resume_file:
        if st.sidebar.button("Parse & Index Resume", key="parse_resume"):
            with st.spinner("Parsing & indexing resume into ChromaDB..."):
                if parse_and_index_resume(resume_file):
                    status = "✅ Indexed into ChromaDB" if st.session_state.resume_indexed else "✅ Parsed (will index after API key set)"
                    st.sidebar.success(status)
                    st.rerun()

    st.sidebar.markdown("---")

    # Job postings upload
    st.sidebar.markdown("### 📋 Upload Job Postings")
    job_files = st.sidebar.file_uploader(
        "Upload job postings (multiple)", type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True, key="job_uploader"
    )
    if job_files:
        if st.sidebar.button("Parse & Index Jobs", key="parse_jobs"):
            with st.spinner("Parsing & indexing job postings..."):
                for jf in job_files:
                    if parse_and_index_job(jf):
                        st.sidebar.success(f"✅ Indexed: {jf.name}")
            st.rerun()

    st.sidebar.markdown("---")

    # Clear controls
    st.sidebar.markdown("### 🗑️ Clear Data")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.conversation_history = []
            st.rerun()
    with c2:
        if st.button("Clear All", key="clear_all"):
            if st.session_state.assistant:
                st.session_state.assistant.reset_store()
            st.session_state.resume_text = None
            st.session_state.resume_filename = None
            st.session_state.resume_indexed = False
            st.session_state.job_postings = {}
            st.session_state.conversation_history = []
            st.session_state.job_counter = 0
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Example Questions")
    st.sidebar.markdown("""
- What skills am I missing for Job #1?
- How does my experience align with Job #2?
- Which job is the best fit for me?
- Help me prepare for an interview for Job #1
- What should I emphasize in my cover letter?
    """)


# ── Main content ───────────────────────────────────────────────────────────────
def display_uploaded_files():
    st.markdown("### 📄 Indexed Documents")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Resume:**")
        if st.session_state.resume_filename:
            badge = "🟢 Indexed" if st.session_state.resume_indexed else "🟡 Parsed (not indexed)"
            st.markdown(f"✅ {st.session_state.resume_filename}  `{badge}`")
        else:
            st.markdown("❌ No resume uploaded")

    with c2:
        st.markdown("**Job Postings:**")
        if st.session_state.job_postings:
            for num, data in st.session_state.job_postings.items():
                badge = "🟢 Indexed" if data.get("indexed") else "🟡 Parsed"
                chunks = data.get("chunks", "?")
                st.markdown(f"✅ Job #{num}: {data['name']}  `{badge}` · {chunks} chunks")
        else:
            st.markdown("❌ No job postings uploaded")

    st.markdown("---")


def display_chat_interface():
    st.markdown("### 💬 Ask Questions")
    for msg in st.session_state.conversation_history:
        css_class = "user-message" if msg["role"] == "user" else "assistant-message"
        label = "You" if msg["role"] == "user" else "Assistant"
        st.markdown(
            f'<div class="chat-message {css_class}"><strong>{label}:</strong> {msg["content"]}</div>',
            unsafe_allow_html=True
        )

    user_input = st.chat_input("Ask about career fit, skill gaps, interview prep…")
    if user_input:
        handle_user_message(user_input)


def main_content():
    st.markdown('<div class="main-header">🎯 Career Intelligence Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">RAG-powered · ChromaDB · GPT-4o-mini</div>', unsafe_allow_html=True)

    display_uploaded_files()

    if not st.session_state.resume_text:
        st.info("👈 Upload your resume in the sidebar to get started!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
**📊 Career Fit Assessment**
- Semantic skill matching via RAG
- Fit scores per job posting
- Ranked job recommendations
""")
        with col2:
            st.markdown("""
**🎓 Skills Gap Analysis**
- Precise gap detection from JD chunks
- Hard & soft skill breakdown
- Learning path suggestions
""")
        with col3:
            st.markdown("""
**💼 Interview Preparation**
- Role-specific question generation
- Talking points from your resume
- Targeted preparation advice
""")

        st.markdown("---")
        st.markdown("### 📖 How It Works (RAG Pipeline)")
        st.markdown("""
1. **Upload & Parse** — Resume and JDs are parsed from PDF/DOCX/TXT
2. **Chunk** — Documents are split into overlapping 500-char chunks
3. **Embed & Index** — Chunks are embedded via OpenAI and stored in **ChromaDB**
4. **Query** — Your question is embedded and matched against relevant chunks
5. **Generate** — Only the most relevant chunks are sent to GPT-4o-mini → precise, cost-efficient answers
""")
    else:
        display_chat_interface()

        if st.session_state.job_postings and st.session_state.assistant:
            st.markdown("---")
            st.markdown("### 🚀 Quick Analysis")
            cols = st.columns(min(len(st.session_state.job_postings), 3))
            for idx, (job_num, job_data) in enumerate(st.session_state.job_postings.items()):
                with cols[idx % 3]:
                    if st.button(f"Analyze Job #{job_num}", key=f"analyze_{job_num}"):
                        with st.spinner(f"Running RAG analysis for Job #{job_num}..."):
                            analysis = st.session_state.assistant.get_quick_analysis(
                                job_num=job_num,
                                job_name=job_data["name"]
                            )
                        st.session_state.conversation_history.append({
                            "role": "user",
                            "content": f"Quick analysis for Job #{job_num}: {job_data['name']}"
                        })
                        st.session_state.conversation_history.append({
                            "role": "assistant",
                            "content": analysis
                        })
                        st.rerun()


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    initialize_session_state()
    sidebar_config()
    main_content()


if __name__ == "__main__":
    main()


