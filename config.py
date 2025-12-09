import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    GENERATION_MODEL: str = "gemini-2.5-flash"
    
    ALLOWED_FILE_TYPES = ['pdf', 'txt', 'md', 'docx', 'doc']
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 80
    TOP_K_RESULTS: int = 5
    
    EMBEDDING_DIMENSION: int = 768

config = Config()
