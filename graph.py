from langgraph.graph import StateGraph, END
from nodes import decide_and_calculate
from typing import TypedDict

class GraphState(TypedDict):
    input: str
    output: str

def run_graph(expression: str):
    builder = StateGraph(GraphState)  

    builder.add_node("calculate", lambda state: {"output": decide_and_calculate(state["input"])})

    builder.set_entry_point("calculate")
    builder.add_edge("calculate", END)

    graph = builder.compile()

    result = graph.invoke({"input": expression})
    print(result["output"])

if __name__ == "__main__":
    run_graph("2+3")
    run_graph("100-9")

