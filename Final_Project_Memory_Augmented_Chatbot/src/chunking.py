import psycopg2
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
DB_CONFIG = f"dbname=chatbot_db user=postgres password={os.getenv('POSTGRES_PASSWORD')} host=localhost"

def chunk_data():
    # 1. Connect and Fetch data
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT content FROM knowledge_base")
    rows = cur.fetchall()
    conn.close()

    # 2. Define the Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
    )

    # 3. Process each row
    all_chunks = []
    for row in rows:
        content = row[0]
        chunks = text_splitter.split_text(content)
        all_chunks.extend(chunks)

    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunks = chunk_data()
    # Print the first 2 chunks to see if they look clean
    print("First chunk:", chunks[0])
    print("Second chunk:", chunks[1])