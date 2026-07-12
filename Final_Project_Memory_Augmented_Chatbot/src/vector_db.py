import chromadb
from sentence_transformers import SentenceTransformer
import psycopg2

# We will use a lightweight model to convert text to numbers
model = SentenceTransformer('all-MiniLM-L6-v2')

def store_chunks_in_chroma(chunks):
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="fastapi_docs")

    # Generate Embeddings and add to Chroma
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk]
        )
    print(f"Successfully stored {len(chunks)} chunks in ChromaDB!")

if __name__ == "__main__":
    # Import the chunk function from your chunking script
    from chunking import chunk_data
    chunks = chunk_data()
    store_chunks_in_chroma(chunks)