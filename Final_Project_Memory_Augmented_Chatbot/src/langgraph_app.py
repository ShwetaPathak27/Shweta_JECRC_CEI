import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults 

# 1. Setup
load_dotenv()

# 2. Tools and Model
# max_results=3 and search_depth="advanced" for better search results
search_tool = TavilySearchResults(max_results=3, search_depth="advanced") 
tools = [search_tool]
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
llm_with_tools = llm.bind_tools(tools)

# 3. State
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# 4. Nodes
def model_node(state):
    # Make sure to include a system message to guide the model's behavior
    system_msg = SystemMessage(content=(
        "You are a helpful and professional AI assistant. "
        "1. First, try to answer using your internal knowledge or provided context. "
        "2. If you do not have sufficient information, use the 'tavily_search' tool to find the information online. "
        "3. If the query is nonsense, politely state that you cannot process it. "
        "Do not invent facts."
    ))
    
    # Combine the system message with the conversation history
    messages = [system_msg] + state["messages"]
    
    try:
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    except Exception as e:
        # If the model fails to respond, return a fallback message
        return {"messages": [AIMessage(content="I am having trouble accessing my search tools, but I'm here to help with other queries!")]}

# 5. Graph
workflow = StateGraph(AgentState)
workflow.add_node("model", model_node)
workflow.add_node("tools", ToolNode(tools))
workflow.set_entry_point("model")
workflow.add_conditional_edges("model", tools_condition)
workflow.add_edge("tools", "model")

app = workflow.compile()

# 6. Test
if __name__ == "__main__":
    query = "What is the latest update on FastAPI 2026?"
    result = app.invoke({"messages": [HumanMessage(content=query)]})
    
    print("\n--- Final Chatbot Answer ---")
    print(result["messages"][-1].content)