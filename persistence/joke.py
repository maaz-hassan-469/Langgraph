from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver

model = ChatOllama(model="llama3.2:1b")

checkpointer = InMemorySaver()


class Joke(TypedDict):
    topic: str
    joke: str
    explanation: str


def generate_joke(state: Joke):
    prompt = f"Generate a joke on the following topic: {state['topic']}"

    response = model.invoke(prompt)

    return {"joke": response}


def explanation_joke(state: Joke):
    prompt = f"Write an explanation for the following joke: {state['joke']}"

    response = model.invoke(prompt)

    return {"explanation": response}


graph = StateGraph(Joke)

graph.add_node("generate_joke", generate_joke)
graph.add_node("explanation_joke", explanation_joke)

graph.add_edge(START, "generate_joke")
graph.add_edge("generate_joke", "explanation_joke")
graph.add_edge("explanation_joke", END)

workflow = graph.compile(checkpointer=checkpointer)


config1 = {
    "configurable": {
        "thread_id": "1"
    }
}

result = workflow.invoke(
    {"topic": "pizza"},
    config=config1
)

print(workflow.get_state(config1))