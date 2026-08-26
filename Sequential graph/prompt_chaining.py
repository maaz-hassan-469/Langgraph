from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from typing import TypedDict

model=ChatOllama(model="llama3.2:1b", temperature=0.1)

class llmstate(TypedDict):
    question:str
    answer:str
    content:str

graph=StateGraph(llmstate)

def LLM(state:llmstate)->llmstate:
    topic=state["question"]
    query=f"answer the following question {topic}"

    answer=model.invoke(query)
    state["answer"]=answer
    return state

def LLMcontent(state:llmstate)->llmstate:
    title=state["question"]
    outline=state["answer"]
    query=f"give me blog on this {title} using the following {outline}"
    content=model.invoke(query).content
    state["content"]=content
    return state


graph.add_node("LLM",LLM)
graph.add_node("LLMcontent",LLMcontent)

graph.add_edge(START,"LLM")
graph.add_edge("LLM","LLMcontent")
graph.add_edge("LLMcontent",END)

workflow=graph.compile()

ans=workflow.invoke({"question":"give me outlineof the topic terrorism"})
print(ans["answer"])

