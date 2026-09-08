from langgraph.graph import StateGraph,START,END
from typing import TypedDict

class batsmanstate(TypedDict):
    balls:int
    runs:int
    fours:int
    sixes:int
    sr:float
    bpb:float
    boundary_percent:float
    summary:str


graph=StateGraph(batsmanstate)

def calculate_sr(state:batsmanstate):
    sr=(state["runs"]/state["balls"])*100
    return {"sr":sr}

def calculate_bpb(state:batsmanstate):
    bpb=state["balls"]/(state["fours"]+state["sixes"])
    return {"bpb":bpb}

def calculate_boundary_percent(state:batsmanstate):
    boundary_percent=(((state["fours"]*4)+(state["sixes"]*6))/(state["runs"]))*100
    return {"boundary_percent":boundary_percent}

def summary(state:batsmanstate):
    summary=f""" strike rate:{state["sr"]},
    balls per boundary :{state["bpb"]},
    boundary percent:{state["boundary_percent"]}"""
    

    return {"summary":summary}


graph.add_node("calculate_sr",calculate_sr)
graph.add_node("calculate_bpb",calculate_bpb)
graph.add_node("calculate_boundary_percent",calculate_boundary_percent)
graph.add_node("summary",summary)


graph.add_edge(START,"calculate_sr")
graph.add_edge(START,"calculate_bpb")
graph.add_edge(START,"calculate_boundary_percent")
graph.add_edge("calculate_sr","summary")
graph.add_edge("calculate_bpb","summary")
graph.add_edge("calculate_boundary_percent","summary")

graph.add_edge("summary",END)

workflow=graph.compile()

initial_state={"balls":100,"runs":200,"fours":10,"sixes":5}
ans=workflow.invoke(initial_state)
print(ans)