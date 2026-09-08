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


graph=StateGraph(batsmanstate)

def calculate_sr(state:batsmanstate):
    sr=(state["runs"]/state["balls"])*100
    state["sr"]=sr
    return state["sr"]

def calculate_bpb(state:batsmanstate):
    bpb=state["balls"]/(state["fours"]+state["sixes"])
    state["bpb"]=bpb
    return state["bpb"]

def calculate_boundary_percent(state:batsmanstate):
    boundary_percent=(((state["fours"]*4)+(state["sixes"]*6))/(state["runs"]))*100
    state["boundary_percent"]=boundary_percent
    return state["boundary_percent"]

def summary(state:batsmanstate):
    summary=f""" strike rate:{state["sr"]},
    balls per boundary :{state["bpb"]},
    boundary percent:{state["boundary_percent"]}"""
    state["summary"]=summary

    return state["summary"]


graph.add_node("calculate_sr",calculate_sr)
graph.add_node("calculate_bpb",calculate_bpb)
graph.add_node("calculate_boundary_percent",calculate_boundary_percent)
graph.add_node("summary",summary)
