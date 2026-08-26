from langgraph.graph import StateGraph,START,END
from typing import TypedDict

class BMI(TypedDict):
    height:float
    weight:float
    bmi:float
    category:str

graph=StateGraph(BMI)

def calculate_bmi(state:BMI)->BMI:
    weight=state['weight']
    height=state["height"]
    bmi=weight/(height**2)
    state["bmi"]=round(bmi,2)
    return state

def label_bmi(state:BMI)-> BMI:
    bmi=state["bmi"]
    if bmi<18.5:
       state["category"]="underweight"
    elif  18.5 <=bmi<25:
        state["category"]="normal"
    else:
        state["category"]="obese"
    return state


#add node
graph.add_node("calculate_bmi",calculate_bmi)
graph.add_node("label_bmi",label_bmi)
#add edges
graph.add_edge(START,"calculate_bmi")
graph.add_edge("calculate_bmi","label_bmi")
graph.add_edge("label_bmi",END)

#compile graph
workflow=graph.compile()

#execute graph
output_state=workflow.invoke({"weight":60.5,"height":2})
print(output_state)




