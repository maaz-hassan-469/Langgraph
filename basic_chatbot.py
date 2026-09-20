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

initial_state={
    "messages":[HumanMessage(content="what is the capital of pakistan ")]
}

result=workflow.invoke(initial_state)["messages"][-1].content
print(result)
