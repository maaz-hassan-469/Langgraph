from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict
from pydantic import BaseModel,Field

model=ChatOllama(model="llama3.2:1b", temperature=0.1)

class Evaluationschema(BaseModel):
    feedback:str=Field(description="detailed feedback for the essay")
    score:int=Field(description="score out of 10 ",ge=0,le=10)

structured_model=model.with_structured_output(Evaluationschema)
essay="this essay is about terrorism and its impact on society. It discusses the various forms of terrorism, the reasons behind it, and the measures taken by governments to combat it. The essay also highlights the importance of international cooperation in addressing the issue of terrorism. Overall, the essay provides a comprehensive overview of the topic and emphasizes the need for a collective effort to tackle terrorism effectively."

prompt=f"""evaluate the language quality of the following essay and provide detailed feedback and score out of 10 {essay}"""

ans=structured_model.invoke(prompt)

print(ans)
