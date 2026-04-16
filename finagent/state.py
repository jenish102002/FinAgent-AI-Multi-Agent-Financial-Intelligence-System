from typing import TypedDict, Any

# ==========================================
# INTERNAL ORCHESTRATION SCHEMA (LANGGRAPH)
# ==========================================


class GraphState(TypedDict, total=False):
    """
    Explicit TypedDict for LangGraph internal state.
    We CANNOT use the Pydantic AgentRequest directly because LangGraph passes Pydantic models as object instances,
    which breaks all Python code using `state.get("key")` inside the agents.
    """
    user_query: str
    user_name: str
    amount: float
    avg_amount: float
    frequency: int
    usual_frequency: int
    location: str
    usual_location: str
    country: str
    credit_score: int
    debt: float
    income: float
    risk_profile: str
    market_ticker: str
    intent: str
    plan: dict
    fraud_result: dict
    risk_result: dict
    compliance_result: dict
    advisory_result: dict
    final_decision: dict