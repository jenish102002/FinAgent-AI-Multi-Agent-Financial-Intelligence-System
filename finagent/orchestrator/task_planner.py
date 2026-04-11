import os
import logging
from typing import Dict
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)

# 1. Initialize NVIDIA Chat Model
try:
    # Using ChatNVIDIA directly for better performance with NIM endpoints
    planner_llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0
    )
    
    # 2. Refined Orchestration Prompt
    # Added explicit logic rules to help the 8B model make better decisions
    planner_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a high-level financial orchestration planner.
        Your goal is to decide which agents are necessary to process a user request.
        
        AVAILABLE AGENTS: fraud, risk, compliance, advisory

        CRITICAL OVERRIDE RULES (You MUST obey these):
        1. If the 'Provided Data' field contains ANY of 'credit_score', 'debt', or 'income', you MUST output 'risk'.
        2. If the 'Provided Data' field contains 'country' or 'usual_location', you MUST output 'compliance'.
        3. If 'amount' and 'location' mismatch triggers are present, you MUST output 'fraud'.
        
        GENERAL INTENT RULES:
        - Loan queries -> [risk, compliance]
        - Stock/ticker queries -> [advisory]
        - Large transfers -> [fraud, compliance]
        - General advice (e.g. buying a car, planning) -> [advisory]

        OUTPUT FORMAT:
        Return ONLY a comma-separated list of agent names based on BOTH the Intent/Query and the Provided Data.
        Example output: advisory, risk, compliance
        No other text."""),
        ("human", "Intent: {intent}\nQuery: {query}\nProvided Data: {provided_data}")
    ])
    
    planner_chain = planner_prompt | planner_llm

except Exception as e:
    logging.warning(f"Failed to initialize NVIDIA Planner LLM: {e}")
    planner_chain = None


def task_planner(state: Dict) -> Dict:
    """
    Orchestration node that determines the parallel execution path.
    """
    # Fallback to advisory if state is missing data
    intent = state.get("intent", "advisory")
    query = state.get("user_query", "")
    
    # Default execution list
    selected_agents = ["advisory"]
    
    logging.info(f"Incoming state to Task Planner: {state}")
    
    if planner_chain:
        try:
            # Extract optional keys so the planner knows there's explicit context
            provided_keys = {
                k: v for k, v in state.items() 
                if v and k not in ("user_query", "intent", "plan")
            }
            provided_data_str = ", ".join([f"{k}: {v}" for k, v in provided_keys.items()]) if provided_keys else "None"

            # Invoke the planner
            res = planner_chain.invoke({
                "query": query, 
                "intent": intent, 
                "provided_data": provided_data_str
            })
            content = res.content.strip().lower()
            
            # 3. Robust Parsing
            valid_agents = {"fraud", "risk", "compliance", "advisory"}
            
            # Split by comma, remove dots/spaces, and validate against the agent list
            parsed_agents = [
                agent.strip() 
                for agent in content.replace(".", "").split(",") 
                if agent.strip() in valid_agents
            ]
            
            if parsed_agents:
                selected_agents = list(set(parsed_agents)) # Unique list
                logging.info(f"Planner selected agents: {selected_agents}")
            
        except Exception as e:
            logging.error(f"Task planner LLM invocation failed: {e}")
            # Do not crash the graph; fallback to advisory
            selected_agents = ["advisory"]
    else:
        logging.error("Planner Chain is offline. Defaulting to advisory.")
        selected_agents = ["advisory"]

    # 4. Construct the Plan
    plan = {
        "agents": selected_agents,
        "execution": "parallel"
    }

    return {
        **state,
        "plan": plan
    }