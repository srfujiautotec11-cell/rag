import psycopg
from typing import Optional
from config import config
from pgvector.psycopg import register_vector

class Database:
    def __init__(self):
        self.conn: Optional[psycopg.Connection] = None
    
    def connect(self):
        if not self.conn or self.conn.closed:
            self.conn = psycopg.connect(config.DATABASE_URL)
            register_vector(self.conn)
        return self.conn
    
    def get_cursor(self):
        conn = self.connect()
        return conn.cursor()
    
    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()

db = Database()
