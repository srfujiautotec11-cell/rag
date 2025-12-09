import hashlib
import fitz  # PyMuPDF
import io
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import config

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )

    def extract_text(self, file_source: str | io.BytesIO, file_type: str) -> str:
        """Extracts text from a file source (path or stream) based on its type."""
        if file_type == "pdf":
            # PyMuPDF can open from a path or a stream
            doc = fitz.open(stream=file_source, filetype="pdf")
            text = "".join(page.get_text() for page in doc)
            doc.close()
            return text
        elif file_type in ["doc", "docx"]:
            # python-docx can open from a path or a stream
            doc = Document(file_source)
            return "\n".join([para.text for para in doc.paragraphs])
        elif file_type in ["txt", "md"]:
            # For local file paths (from auto-ingestion)
            with open(file_source, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def chunk_text(self, text: str) -> list[str]:
        """Splits text into manageable chunks."""
        return self.text_splitter.split_text(text)

    def compute_file_hash(self, file_content: bytes) -> str:
        """Computes the SHA256 hash of file content to detect duplicates."""
        hasher = hashlib.sha256()
        hasher.update(file_content)
        return hasher.hexdigest()

document_processor = DocumentProcessor()