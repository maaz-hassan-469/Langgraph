from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict,Literal
from pydantic import BaseModel,Field

model=ChatOllama(model="llama3.2:1b")

class sentimentschema(BaseModel):
    sentiment:Literal["postive",'negative']=Field(description="sentiment of the review")

class reviewstate(TypedDict):
    review:str
    sentiment:Literal['positive','negative']
    diagnosis:dict
    response:str

structured_model1=model.with_structured_output(sentimentschema)

def find_sentiment(state:reviewstate):
    prompt=f"find the sentiment of the following review and return it in a structured format {state['review']}"
    sentiment=structured_model1.invoke(prompt).sentiment
    return {"sentiment":sentiment}

def check_sentiment(state:reviewstate)->Literal["positive_response","run_diagnosis"]:
    if state["sentiment"]=="positive":
        return "positive_response"
    else:
        return "run_diagnosis"

def positive_response(state:reviewstate):
    prompt=f"the following review is positive, generate a response to the review {state['review']}"
    response=model.invoke(prompt)
    return {"response":response}


graph=StateGraph(reviewstate)

graph.add_node("find_sentiment",find_sentiment)
graph.add_node("find_sentiment")

