from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict
import time

class crashstate(TypedDict):
    input:str
    step1:str
    step2:str
    step3:str

graph=StateGraph(crashstate)

def step1(state:crashstate)->crashstate:
    print("step1 executed")
    return {"step1":"done","input":state["input"]}


def step2(state:crashstate)->crashstate:
    print("step2 hanging....and now manually interupt from the notebook tool bar(stop button)")
    time.sleep(30)
    return {"step2":"done"}

def step3(state:crashstate)->crashstate:
    print("step3 executed")

    return{"done":True}

graph.add_node("step1",step1)
graph.add_node("step2",step2)
graph.add_node("step3",step3)

graph.add_edge(START,"step1")
graph.add_edge("step1","step2")
graph.add_edge("step2","step3")
graph.add_edge("step3",END)

checkpointer=InMemorySaver()
workflow=graph.compile(checkpointer=checkpointer)

try:
    print("running graph: please manually interupt during step2")
    graph.invoke({"input":"start"},config={"configurable":{"thread_id":"thread-1"}})
except:
    print("manually interupted")

print(workflow.get_state({"configurable":{"thread_id":"thread-1"}}))
