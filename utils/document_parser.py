

"""Document parsing utilities for PDF, DOCX, and TXT files with chunking support."""

import os
from typing import List
import PyPDF2
from docx import Document
import io
import re


class DocumentParser:
    """Parse documents and extract text content."""

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")

    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:
        try:
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")

    @staticmethod
    def parse_txt(file_bytes: bytes) -> str:
        try:
            return file_bytes.decode('utf-8').strip()
        except UnicodeDecodeError:
            try:
                return file_bytes.decode('latin-1').strip()
            except Exception as e:
                raise Exception(f"Error parsing TXT: {str(e)}")

    @classmethod
    def parse_file(cls, file_bytes: bytes, file_name: str) -> str:
        extension = os.path.splitext(file_name)[1].lower()
        if extension == '.pdf':
            return cls.parse_pdf(file_bytes)
        elif extension == '.docx':
            return cls.parse_docx(file_bytes)
        elif extension == '.txt':
            return cls.parse_txt(file_bytes)
        else:
            raise ValueError(f"Unsupported file format: {extension}")

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for RAG indexing.

        Args:
            text: Full document text
            chunk_size: Max characters per chunk
            chunk_overlap: Overlap between consecutive chunks

        Returns:
            List of text chunks
        """
        # Clean up excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text).strip()

        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at a sentence or newline boundary
            if end < len(text):
                boundary = max(
                    chunk.rfind('\n'),
                    chunk.rfind('. '),
                    chunk.rfind('? '),
                    chunk.rfind('! ')
                )
                if boundary > chunk_size // 2:
                    end = start + boundary + 1
                    chunk = text[start:end]

            chunks.append(chunk.strip())
            start = end - chunk_overlap

        return [c for c in chunks if c]

