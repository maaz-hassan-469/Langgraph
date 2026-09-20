from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated,List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage
from langgraph.graph.message import add_messages

model=ChatOllama(model="llama3.2:1b")

class llmstate(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

graph=StateGraph(llmstate)

def chatbot(state:llmstate):
    messages=state["messages"]
    response=model.invoke(messages)
    return {"messages":[response]}


graph.add_node("chatbot",chatbot)

graph.add_edge(START,"chatbot")
graph.add_edge("chatbot",END)

workflow=graph.compile()

while True:
    user_message=input("type here:")
    if user_message.strip().lower() in ["exit","bye","quit"]:
        break

    response=workflow.invoke({"messages":[HumanMessage(content=user_message)]})
    print("AI:",response["messages"][-1].content)






