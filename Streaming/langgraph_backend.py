from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

llm = ChatOllama(model="llama3.2:1b")

class chatstate(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: chatstate):
    # Using invoke works, but llm.stream() inside the node handles streaming best
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

checkpointer = InMemorySaver()
graph = StateGraph(chatstate)

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chat_bot = graph.compile(checkpointer=checkpointer)

