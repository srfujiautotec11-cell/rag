import psycopg
from config import config

def initialize_database():
    """
    Connects to the database, enables the vector extension,
    and creates the necessary tables for the RAG system.
    """
    try:
        # Connect to the database
        conn = psycopg.connect(config.DATABASE_URL)
        cursor = conn.cursor()

        print("Enabling vector extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        print("Creating 'documents' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                file_type VARCHAR(50),
                category VARCHAR(100),
                file_hash VARCHAR(64) UNIQUE,
                upload_date TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        print("Creating 'chunks' table...")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS chunks (
                id SERIAL PRIMARY KEY,
                document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
                chunk_text TEXT,
                embedding VECTOR({config.EMBEDDING_DIMENSION})
            );
        """)

        # Commit the changes
        conn.commit()
        
        print("✅ Database initialization successful!")

    except Exception as e:
        print(f"❌ An error occurred during database initialization: {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    initialize_database()
