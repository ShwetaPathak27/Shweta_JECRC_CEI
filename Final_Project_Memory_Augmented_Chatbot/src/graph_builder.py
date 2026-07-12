import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from chunking import chunk_data

load_dotenv()

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = os.getenv("NEO4J_PASSWORD") 

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def build_graph():
    chunks = chunk_data()
    with driver.session() as session:
        for i, chunk in enumerate(chunks[:50]): 
            # This query creates a node for each chunk and links it to a concept node
            session.run("""
                MERGE (c:Chunk {id: $id})
                SET c.text = $text
                MERGE (con:Concept {name: 'FastAPI'})
                MERGE (c)-[:MENTIONS]->(con)
            """, id=i, text=chunk)
    print("Graph lines created successfully!")

if __name__ == "__main__":
    build_graph()