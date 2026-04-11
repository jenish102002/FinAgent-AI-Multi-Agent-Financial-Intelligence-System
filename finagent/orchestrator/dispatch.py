import asyncio

from agents.fraud_agent import fraud_agent
from agents.risk_agent import risk_agent
from agents.compliance_agent import compliance_agent
from agents.advisory_agent import advisory_agent


# Map agent names → functions
AGENT_REGISTRY = {
    "fraud": fraud_agent,
    "risk": risk_agent,
    "compliance": compliance_agent,
    "advisory": advisory_agent,
}


async def run_agent(agent_name: str, state: dict):
    """
    Runs a single agent safely
    """
    try:
        func = AGENT_REGISTRY[agent_name]
        result = await asyncio.to_thread(func, state)
        return result
    except Exception as e:
        return {f"{agent_name}_result": {"error": str(e)}}


async def dispatch(state: dict):
    """
    LangGraph Node: Parallel Dispatch
    """
    plan = state.get("plan", {})
    agents = plan.get("agents", [])
    execution = plan.get("execution", "parallel")

    if execution == "single":
        # Run only first agent
        result = await run_agent(agents[0], state)
        state.update(result)
        return state

    # Parallel execution
    tasks = [run_agent(agent, state) for agent in agents]
    results = await asyncio.gather(*tasks)

    for res in results:
        state.update(res)

    return state