from typing import List, Dict, Optional, Tuple
from infra.database import db
from services.embeddings import embedding_service
import json

class VectorStore:
    def store_document(self, filename: str, file_type: str, category: str, file_hash: str) -> int:
        conn = None
        try:
            conn = db.connect()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id FROM documents WHERE file_hash = %s
                    """,
                    (file_hash,)
                )
                existing = cur.fetchone()
                
                if existing:
                    document_id = existing[0]
                    # If document exists, delete old chunks to ensure a clean re-import.
                    cur.execute("DELETE FROM chunks WHERE document_id = %s", (document_id,))
                    return document_id
                
                cur.execute(
                    """
                    INSERT INTO documents (filename, file_type, category, file_hash)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (filename, file_type, category, file_hash)
                )
                conn.commit()
                result = cur.fetchone()
                if result:
                    return result[0]
                raise Exception("Failed to insert document")
        except Exception as e:
            if conn and not conn.closed:
                conn.rollback()
            raise Exception(f"Database error while storing document: {str(e)}")
    
    def store_chunks(self, document_id: int, chunks: List[str], embeddings: List[List[float]]):
        conn = None
        try:
            conn = db.connect()
            with conn.cursor() as cur:
                for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    cur.execute(
                        """
                        INSERT INTO chunks (document_id, chunk_text, embedding)
                        VALUES (%s, %s, %s)
                        """,
                        (document_id, chunk, embedding)
                    )
                conn.commit()
        except Exception as e:
            if conn and not conn.closed:
                conn.rollback()
            raise Exception(f"Database error while storing chunks: {str(e)}")
    
    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        try:
            conn = db.connect()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT 
                        c.id,
                        c.chunk_text,
                        d.filename,
                        d.category,
                        1 - (c.embedding <=> %s::vector) as similarity
                    FROM chunks c
                    JOIN documents d ON c.document_id = d.id
                    ORDER BY c.embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (query_embedding, query_embedding, top_k)
                )
                results = []
                for row in cur.fetchall():
                    results.append({
                        "chunk_id": row[0],
                        "text": row[1],
                        "filename": row[2],
                        "category": row[3],
                        "similarity": float(row[4])
                    })
                return results
        except Exception as e:
            raise Exception(f"Database error during similarity search: {str(e)}")
    
    def get_all_documents(self) -> List[Dict]:
        conn = db.connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    d.id, 
                    d.filename, 
                    d.file_type, 
                    d.category, 
                    d.upload_date, 
                    COUNT(c.id) as total_chunks
                FROM documents d
                LEFT JOIN chunks c ON d.id = c.document_id
                GROUP BY d.id
                ORDER BY d.upload_date DESC
                """
            )
            results = []
            for row in cur.fetchall():
                results.append({
                    "id": row[0],
                    "filename": row[1],
                    "file_type": row[2],
                    "category": row[3],
                    "upload_date": row[4],
                    "total_chunks": row[5]
                })
            return results
    
    def delete_document(self, document_id: int):
        conn = None
        try:
            conn = db.connect()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM documents WHERE id = %s", (document_id,))
                conn.commit()
        except Exception as e:
            if conn and not conn.closed:
                conn.rollback()
            raise Exception(f"Database error while deleting document: {str(e)}")

vector_store = VectorStore()
