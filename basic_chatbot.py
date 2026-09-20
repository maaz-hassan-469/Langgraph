from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated,List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

model=ChatOllama(model="llama3.2:1b")

class llmstate(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

checkpointer=MemorySaver()
graph=StateGraph(llmstate)

def chatbot(state:llmstate):
    messages=state["messages"]
    response=model.invoke(messages)
    return {"messages":[response]}


graph.add_node("chatbot",chatbot)

graph.add_edge(START,"chatbot")
graph.add_edge("chatbot",END)

workflow=graph.compile(checkpointer=checkpointer)

thread_id="1"
while True:
    user_message=input("type here:")
    if user_message.strip().lower() in ["exit","bye","quit"]:
        break
    config={"configurable":{"thread_id":thread_id}}
    response=workflow.invoke({"messages":[HumanMessage(content=user_message)]},config=config)
    print("AI:",response["messages"][-1].content)






