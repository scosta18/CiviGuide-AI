from typing import TypedDict
from app.agents.retrieval_agent import retrieve
from app.agents.eligibility_agent import eligibility
from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
    question: str
    chunks: list[dict]
    draft: str

def retrieve_node(state: GraphState) -> GraphState:
    state["chunks"] = retrieve(state["question"])
    return state

def reason_node(state: GraphState) -> GraphState:
    state["draft"] = eligibility(state["question"], state["chunks"])
    return state


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("reason", reason_node)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "reason")
    graph.add_edge("reason", END)
    return graph.compile()

_compiled_graph = None

def run(question: str) -> GraphState:
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph.invoke({"question": question, "chunks": [], "draft": ""})