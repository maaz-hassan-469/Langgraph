from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
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

# Fix: Stream using stream_mode="messages" safely
for message_chunk, metadata in chat_bot.stream(
    {"messages": [HumanMessage(content="what is the recipe to make pasta")]},
    config={"configurable": {"thread_id": "thread_1"}},
    stream_mode="messages"
):
    if message_chunk.content:
        print(message_chunk.content, end="", flush=True)