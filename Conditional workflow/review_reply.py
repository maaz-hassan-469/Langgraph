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

class diagnosisschema(BaseModel):
    issue_type:Literal["UX","performance","Bug","Support","other"]=Field(description="type of issue")
    tone:Literal["polite","neutral","angry","disappointed","calm"]=Field(description="tone of the review")
    urgency:Literal["high","medium","low"]=Field(description="urgency of the issue")


structured_model1=model.with_structured_output(sentimentschema)
structured_model2=model.with_structured_output(diagnosisschema)

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

def run_diagnosis(state:reviewstate):
    prompt=f"the following review is negative, diagnose the issue and return it in a structured format {state['review']}"
    response=structured_model2.invoke(prompt)
    return {"diagnosis":response.model_dump()}
def negative_response(state:reviewstate):
    prompt=f"the following review is negative, generate a response to the review {state['review']} and address the issue {state['diagnosis']}"
    response=model.invoke(prompt)
    return {"response":response}

graph=StateGraph(reviewstate)

graph.add_node("find_sentiment",find_sentiment)
graph.add_node("negative_response",negative_response)
graph.add_node("positive_response",positive_response)
graph.add_node("run_diagnosis",run_diagnosis)

graph.add_edge(START,"find_sentiment")
graph.add_conditional_edges("find_sentiment",check_sentiment)
graph.add_edge("positive_response",END)
graph.add_edge("run_diagnosis","negative_response")
graph.add_edge("negative_response",END)

workflow=graph.compile()

initial_state={
    'review':"i have been using this app for about a month now,and i must say the user interface is incredibily clean and easy to use everything is exactly where you would expect to be"
}

result=workflow.invoke(initial_state)
print(result)