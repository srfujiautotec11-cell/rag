import google.generativeai as genai
from typing import List, Dict
from config import config

class GeneratorService:
    def __init__(self):
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GENERATION_MODEL)
    
    def generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        context_text = "\n\n".join([
            f"[Source: {chunk['filename']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        prompt = f"""You are a helpful assistant that answers questions based on the provided context from the user's personal knowledge base.

Context from documents:
{context_text}

User Question: {query}

Instructions:
- Answer the question using ONLY the information provided in the context above.
- If the context doesn't contain enough information to answer the question, say so clearly.
- Cite which sources you used (mention the filename) when providing information.
- Be concise but complete in your answer.

Answer:"""
        
        response = self.model.generate_content(prompt)
        return response.text

generator_service = GeneratorService()
