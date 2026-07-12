# KnoGraph AI : Memory-Augmented Hybrid RAG Assistant

KnoGraph AI is an advanced, agentic RAG (Retrieval-Augmented Generation) assistant designed for real-time, context-aware information retrieval. It integrates private knowledge base querying with live internet search capabilities, all while maintaining conversational memory.

##  Data Engineering Pipeline
* **Web Scraping:** Built a custom scraper to extract domain-specific data from target sources.
* **Data Cleaning & ETL:** Performed rigorous data cleaning to structure unstructured text into a clean format.
* **Knowledge Graph Construction:**
    * **PostgreSQL:** Used as the primary relational store for raw processed data.
    * **Neo4j:** Leveraged for structured knowledge representation, creating complex relationships between entities to enable graph-based reasoning.
* **Vector Integration:** Data indexed into a vector database to enable hybrid (semantic + graph) retrieval.

## Key Features
* **Hybrid RAG Pipeline:** Combines local vector storage with dynamic web search via Tavily.
* **Agentic Reasoning:** Uses LangGraph to manage stateful decision-making and tool-use.
* **Multimodal Interaction:** Supports both text and voice-based input/output (gTTS integration).
* **Memory-Aware:** Retains chat history across sessions using Streamlit session states.
* **Professional UI:** A clean, fixed-footer responsive interface designed for seamless UX.

## Tech Stack
* **Frameworks:** FastAPI, LangGraph, LangChain, Streamlit.
* **Data & Graph:** PostgreSQL, Neo4j, Chroma/Vector DB.
* **LLM & AI:** Groq (llama-3.3-70b-versatile), Tavily Search API.
* **Voice:** Google Text-to-Speech (gTTS), SpeechRecognition.
* **Storage:** RAM-based streaming for audio responses to optimize storage.

##  System Architecture & Evaluation (Step 7)
The system is evaluated based on three primary metrics:
1. **Response Latency:** Optimized using asynchronous API calls (`FastAPI async`) and RAM-based audio buffering.
2. **Contextual Accuracy:** Achieved via hybrid retrieval, ensuring the model prioritizes local knowledge before triggering external tools.
3. **Robustness:** Implemented 'Adaptive Fallback Mechanisms'—if a tool fails, the system automatically redirects to the base LLM rather than crashing.

## Note: Please create a .env file in the project root directory and add the following keys to run the application:"
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
NEO4J_PASSWORD=your_neo4j_password
POSTGRES_PASSWORD=your_postgres_password

##  How to Run
1. **Backend:**
   python  uvicorn src.api:api --reload

2. Frontend:
   streamlit run ui.py

##  Conclusion
KnoGraph AI demonstrates the integration of modern AI paradigms—RAG, knowledge graphs, memory systems, and tool-based reasoning—into a single unified architecture. It reflects real-world AI system design.