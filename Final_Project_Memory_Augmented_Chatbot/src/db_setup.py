import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to your database
def init_db():
    try:
        conn = psycopg2.connect(
            dbname="chatbot_db", 
            user="postgres", 
            password=os.getenv("POSTGRES_PASSWORD"), 
            host="localhost"
        )
        cur = conn.cursor()
        
        # Create table for our scraped content
        cur.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE,
                content TEXT
            );
        """)
        
        # Create table for user memory
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_memory (
                id SERIAL PRIMARY KEY,
                user_id TEXT,
                preference TEXT
            );
        """)
        
        conn.commit()
        print("Database tables created successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    init_db()