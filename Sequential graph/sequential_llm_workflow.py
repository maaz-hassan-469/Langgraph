from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from typing import TypedDict

model=ChatOllama(model="llama3.2:1b", temperature=0.1)

class llmstate(TypedDict):
    question:str
    answer:str

graph=StateGraph(llmstate)

def LLM(state:llmstate)->llmstate:
    topic=state["question"]
    query=f"answer the following question {topic}"

    answer=model.invoke(query)
    state["answer"]=answer
    return state

graph.add_node("LLM",LLM)

graph.add_edge(START,"LLM")
graph.add_edge("LLM",END)

workflow=graph.compile()

ans=workflow.invoke({"question":"give me outlineof the topic terrorism"})
print(ans["answer"])

