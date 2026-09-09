from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict,List,Annotated
from pydantic import BaseModel,Field
import operator

model=ChatOllama(model="llama3.2:1b", temperature=0.1)

class Evaluationschema(BaseModel):
    feedback:str=Field(description="detailed feedback for the essay")
    score:int=Field(description="score out of 10 ",ge=0,le=10)

class state(TypedDict):
    essay:str
    language_feedback:str
    analysis_feedback:str
    clarity_feedback:str
    overall_feedback:str
    individual_scores:Annotated[List[int],operator.add]
    avg_score:float
    
structured_model=model.with_structured_output(Evaluationschema)
essay="this essay is about terrorism and its impact on society. It discusses the various forms of terrorism, the reasons behind it, and the measures taken by governments to combat it. The essay also highlights the importance of international cooperation in addressing the issue of terrorism. Overall, the essay provides a comprehensive overview of the topic and emphasizes the need for a collective effort to tackle terrorism effectively."


graph=StateGraph(state)

def evaluate_language(state:state):
    query=f"evaluate the language quality of the following essay and provide detailed feedback and score out of 10 {state['essay']}"
    response=structured_model.invoke(query)
    return {"language_feedback":response.feedback,"individual_scores":[response.score]}

def evaluate_analysis(state:state):
    query=f"evaluate the depth of analysis of the following essay and provide detailed feedback and score out of 10 {state['essay']}"
    response=structured_model.invoke(query)
    return {"analysis_feedback":response.feedback,"individual_scores":[response.score]}

def evaluate_thought(state:state):
    query=f"evaluate the clarity of thought of the following essay and provide detailed feedback and score out of 10 {state['essay']}"
    response=structured_model.invoke(query)
    return {"clarity_feedback":response.feedback,"individual_scores":[response.score]}

def final_evaluation(state:state):
    prompt=f"""based on the following feedbacks create a summarized feedback \n language feedback:{state['language_feedback']}\n analysis feedback:{state['analysis_feedback']}\n clarity feedback:{state['clarity_feedback']}
"""
    overall_feedback=structured_model.invoke(prompt).content
    avg_score=sum(state["individual_scores"])/len(state["individual_scores"])
    return {"overall_feedback":overall_feedback,"avg_score":avg_score}



graph.add_node("evaluate_language",evaluate_language)
graph.add_node("evaluate_analysis",evaluate_analysis)
graph.add_node("evaluate_thought",evaluate_thought)
graph.add_node("final_evaluation",final_evaluation)


