from langgraph.graph import StateGraph, END

from orchestrator.intent_parser import intent_parser
from orchestrator.task_planner import task_planner
from orchestrator.dispatch import dispatch
from orchestrator.aggregator import aggregator


def build_graph():
    builder = StateGraph(dict)

    builder.add_node("intent", intent_parser)
    builder.add_node("plan", task_planner)
    builder.add_node("dispatch", dispatch)
    builder.add_node("aggregate", aggregator)

    builder.set_entry_point("intent")

    builder.add_edge("intent", "plan")
    builder.add_edge("plan", "dispatch")
    builder.add_edge("dispatch", "aggregate")
    builder.add_edge("aggregate", END)

    return builder.compile()