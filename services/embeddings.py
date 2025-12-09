import google.generativeai as genai
from typing import List
from config import config

class EmbeddingService:
    def __init__(self):
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = config.EMBEDDING_MODEL
    
    def generate_embedding(self, text: str) -> List[float]:
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def generate_query_embedding(self, query: str) -> List[float]:
        result = genai.embed_content(
            model=self.model,
            content=query,
            task_type="retrieval_query"
        )
        return result['embedding']
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embeddings.append(self.generate_embedding(text))
        return embeddings

embedding_service = EmbeddingService()
