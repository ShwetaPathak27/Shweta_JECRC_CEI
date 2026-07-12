# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from .langgraph_app import app  #  existing compiled graph
from langchain_core.messages import HumanMessage

api = FastAPI(title="Voice Assistant API")

# Request schema
class ChatRequest(BaseModel):
    query: str

@api.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # LangGraph invoke
        result = app.invoke({"messages": [HumanMessage(content=request.query)]})
        
        # Safely extract content
        if "messages" in result and result["messages"]:
            last_msg = result["messages"][-1]
            response_text = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        else:
            response_text = "I received your query, but could not generate a response."
            
        return {"response": response_text}
    except Exception as e:
        # Give error message in response
        return {"response": f"System error occurred: {str(e)}"}
