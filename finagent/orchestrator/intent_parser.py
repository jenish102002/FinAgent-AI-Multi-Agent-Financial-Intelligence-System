import json
import logging
import os
from typing import Dict

# Required LangChain/NVIDIA imports
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate

# Initialize logging
logging.basicConfig(level=logging.INFO)

# 1. Initialize the NVIDIA LLM 
# Using temperature 0 is critical for extraction to ensure consistency
try:
    llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0
    )
except Exception as e:
    logging.error(f"Failed to initialize NVIDIA LLM for extraction: {e}")
    llm = None

# 2. Define the extraction prompt
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a highly precise financial data extractor. 
    Analyze the user's query and return a valid JSON object with these keys:
    - intent: (one of: fraud_check, loan_approval, compliance_check, advisory)
    - amount: (number or null)
    - market_ticker: (ticker symbol like 'NVDA' or null)
    - country: (ISO code or name, or null)
    - user_name: (string or null)
    - risk_profile: (conservative, moderate, aggressive, or null)

    Rules:
    - If the user mentions a stock but no ticker, try to provide the ticker (e.g., Apple -> AAPL).
    - If no amount is mentioned, use null.
    - Return ONLY the raw JSON. Do not include conversational filler."""),
    ("human", "{query}")
])

# 3. Create the chain
if llm:
    extraction_chain = extraction_prompt | llm
else:
    extraction_chain = None

# 4. The Parser Node
def intent_parser(state: Dict) -> Dict:
    """
    Parses the raw user query into structured data for the sub-agents.
    """
    query = state.get("user_query", "")
    
    # Default state to ensure the graph doesn't break
    default_data = {
        "intent": "advisory",
        "amount": None,
        "market_ticker": None,
        "country": None,
        "user_name": None,
        "risk_profile": "moderate"
    }

    if extraction_chain:
        try:
            res = extraction_chain.invoke({"query": query})
            
            # 1. Clean up the response (strip whitespace and markdown)
            raw_content = res.content.strip()
            if "```" in raw_content:
                raw_content = raw_content.replace("```json", "").replace("```", "").strip()
            
            # 2. Parse JSON
            data = json.loads(raw_content)
            
            # 3. Log extraction for debugging
            logging.info(f"Extracted Entities: {data}")
            
            # Merge extracted entities into the state, but DO NOT overwrite 
            # established explicit UI values with 'None' from the LLM.
            merged_state = state.copy()
            for key, val in data.items():
                if val is not None:
                    # Let the LLM extraction overwrite if it explicitly finds a value
                    merged_state[key] = val
            
            return merged_state
            
        except Exception as e:
            logging.error(f"Entity extraction failed: {e}")
            # Fallback to default structure if parsing fails
            return {**state, **default_data}
    else:
        logging.error("Extraction Chain not initialized. Check NVIDIA_API_KEY.")
        return {**state, **default_data}