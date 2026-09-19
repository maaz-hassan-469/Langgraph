from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict,Literal
from pydantic import BaseModel,Field
from langchain.messages import HumanMessage,SystemMessage

model=ChatOllama(model="llama3.2:1b")

class poststate(TypedDict):
    
