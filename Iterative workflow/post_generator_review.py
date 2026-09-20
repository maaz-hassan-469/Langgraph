from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict,Literal
from pydantic import BaseModel,Field
from langchain.messages import HumanMessage,SystemMessage

model=ChatOllama(model="llama3.2:1b")
class poststate(TypedDict):
    topic:str
    tweet:str
    evaluation:Literal["approved","need_improvement"]
    feedback:str
    iteration:int
    max_iteration:int

class tweetevaluation(BaseModel):
    evaluation:Literal["approved","need_approvement"]=Field(description="final evaluation of the feedback")
    feedback:str=Field(...,description="feedback for the tweet")

evaluator_llm=model.with_structured_output(tweetevaluation)

graph=StateGraph(poststate)

def generate_tweet(state:poststate):
    messages=[SystemMessage(content="you are a funny and clever twitter/X influencer."),
              HumanMessage(content=f"""
write a short,original and hilarious  tweet on the topic : "{state['topic']}" 
rules:
-do not use question-answer format
-max 280 characters 
-use observation humor,irony,sarcasm,or cultural references 
-think in meme logic ,punchlines,or relatable takes
-this is version {state['iteration']+1}
""")]
    response=model.invoke(messages).content
    return {"tweet":response}

def evaluate_tweet(state:poststate):
    prompt=f"""Evaluate the following generated social media post and decide whether it should be approved or needs improvement.

    Post:
    "{state['tweet']}"

    Evaluate it based on these criteria:

    1. Relevance — Does the post clearly match the intended topic and purpose?
    2. Clarity — Is it easy to understand, well-written, and free from confusing wording?
    3. Engagement — Is it interesting enough to capture attention and encourage interaction?
    4. Value — Does it provide useful, meaningful, entertaining, or informative content?
    5. Originality — Does it feel fresh and natural rather than generic or repetitive?
    6. Tone — Is the tone appropriate for the intended audience and platform?
    7. Structure — Is the post well-organized, concise, and easy to read?
    8. Quality — Check for grammar, spelling, awkward phrasing, unnecessary repetition, or weak sentences.
    9. Platform suitability — Does it follow common social-media best practices and avoid unnecessary length or irrelevant content?

    Decision rules:
    - Approve the post only if it satisfies the criteria reasonably well.
    - If there are noticeable weaknesses that could reduce its quality or effectiveness, mark it as "need_improvement".
    - Do not rewrite the post unless necessary to explain what should be improved.

    Respond ONLY in this structured format:

    evaluation: "approved" or "need_improvement"
    feedback: "Briefly explain the main strengths and weaknesses of the post and, if improvement is needed, clearly state what should be changed."""

    response=evaluator_llm.invoke(prompt)
    return {"evaluation":response.evaluation,"feedback":response.feedback}

def optimmize_tweet(state:poststate):
    messages=[SystemMessage(content="You are an expert social media copywriter. Improve the tweet based on the evaluation feedback provided below"),
              HumanMessage(content=f"""Feedback:
    "{state['feedback']}"

    Topic:
    "{state['topic']}"

    Original Tweet:
    "{state['tweet']}"

    Rewrite the tweet as a short, engaging, viral-worthy tweet.

    Requirements:
    - Keep it relevant to the topic.
    - Fix the weaknesses mentioned in the feedback.
    - Make it clear, natural, punchy, and engaging.
    - Improve humor, originality, and shareability where appropriate.
    - Avoid generic or unnecessary wording.
    - Do NOT use Q&A style.
    - Do NOT use setup-punchline joke structure.
    - Keep it under 280 characters.
    - Preserve the original idea when possible rather than changing the topic completely.
    - Output ONLY the improved tweet, with no explanation, labels, or quotation marks.""")]
    response=model.invoke(messages).content
    iteration=state["iteration"]+1    
    return {"tweet":response,"iteration":iteration}

def route_evaluation(state:poststate):
    if state["evaluation"]=="approved" or state["iteration"]>=state["max_iteration"]:
        return "approved"
    else: 
        return "need_improvement" 



graph.add_node("generate",generate_tweet)
graph.add_node("evaluate",evaluate_tweet)
graph.add_node("optimize",optimmize_tweet)

graph.add_edge(START,"generate")
graph.add_edge("generate","evaluate")
graph.add_conditional_edges("evaluate",route_evaluation ,{"approved":END,"need_improvement":"optimize"})
graph.add_edge("optimize","evaluate")

workflow=graph.compile()

initial_state={
    "topic":"pakistan cricket",
    "iteration":0,
    "max_iteration":5
}

result=workflow.invoke(initial_state)
print(result)
