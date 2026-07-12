import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from neo4j import GraphDatabase
import chromadb

# 1. Environment Variables load karein
load_dotenv()

# 2. Groq Setup (Security best practice)
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

# 3. Database Clients (Password load from environment variable for security)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="fastapi_docs")
driver = GraphDatabase.driver(
    "bolt://localhost:7687", 
    auth=("neo4j", os.getenv("NEO4J_PASSWORD"))
)

def get_graph_context(concept):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Chunk)-[:MENTIONS]->(con:Concept {name: $concept}) RETURN c.text", 
            concept=concept
        )
        return [record["c.text"] for record in result]

def ask_bot(question):
    # Retrieval (Vector + Graph)
    vector_results = collection.query(query_texts=[question], n_results=2)
    graph_context = get_graph_context("FastAPI")
    
    # Prompt Construction
    full_context = "\n".join(vector_results['documents'][0]) + "\n" + "\n".join(graph_context)
    prompt = f"Use the provided context to answer the question accurately. If the context is not sufficient, say so.\n\nQuestion: {question}\n\nContext:\n{full_context}"
    
    # Generation
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    # Test question
    user_query = "How to use dependency injection in FastAPI?"
    answer = ask_bot(user_query)
    print(f"\n--- Chatbot Answer ---\n{answer}")