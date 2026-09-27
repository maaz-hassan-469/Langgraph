from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

CONFIG = {"configurable": {"thread_id":"thread_2" }}
llm = ChatOllama(model="llama3.2:1b")

class chatstate(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: chatstate):
    # Using invoke works, but llm.stream() inside the node handles streaming best
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

con=sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer = SqliteSaver(conn=con)

graph = StateGraph(chatstate)

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chat_bot = graph.compile(checkpointer=checkpointer)
def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])

    return list(all_threads)