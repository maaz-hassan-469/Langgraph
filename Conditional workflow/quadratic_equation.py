from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal

class quadstate(TypedDict):

    a:int
    b:int
    c:int

    equation:str
    discriminant:int
    result:int

graph=StateGraph(quadstate)

def get_equation(state:quadstate):
    equation=f"{state['a']}x^2 + {state['b']}x + {state['c']} = 0"
    return {"equation":equation}

def calculate_discriminant(state:quadstate):
    discriminant=state['b']**2 - 4*state['a']*state['c']
    return {"discriminant":discriminant}

def real_roots(state:quadstate):
    root1=(-state['b'] + state['discriminant']**0.5)/(2*state['a'])
    root2=(-state['b'] - state['discriminant']**0.5)/(2*state['a'])
    result=f"the roots of the equation are {root1} and {root2}"
    return {"result":result}

def repeated_roots(state:quadstate):
    root=-state['b']/(2*state['a'])
    result=f"the equation has repeated roots: {root}"
    return {"result":result}

def no_real_roots(state:quadstate):
    result="the equation has no real roots"
    return {"result":result}

def check_condition(state:quadstate)->Literal["real_roots","repeated_roots","no_real_roots"]:
    if state["discriminant"]>0:
        return "real_roots"
    elif state["discriminant"]==0:
        return "repeated_roots"
    else:
        return "no_real_roots"

graph.add_node("get_equation",get_equation)
graph.add_node("calculate_discriminant",calculate_discriminant)
graph.add_node("real_roots",real_roots)
graph.add_node("repeated_roots",repeated_roots)
graph.add_node("no_real_roots",no_real_roots)
graph.add_node("check_condition",check_condition)

graph.add_edge(START,"get_equation")
graph.add_edge("get_equation","calculate_discriminant")
graph.add_conditional_edges("calculate_discriminant",check_condition)
graph.add_edge("real_roots",END)
graph.add_edge("repeated_roots",END)
graph.add_edge("no_real_roots",END)

workflow=graph.compile()

initial_state={"a":5,
               "b":6,
               "c":0}

result=workflow.invoke(initial_state)

print(result)