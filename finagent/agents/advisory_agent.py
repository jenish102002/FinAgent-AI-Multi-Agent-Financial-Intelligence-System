import os
import logging
from typing import Dict

import yfinance as yf
# Only need ChatNVIDIA now, no need for Embeddings, FAISS, or Document Loaders
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate

# Initialize logging
logging.basicConfig(level=logging.INFO)

# 1. Initialize NVIDIA LLM
try:
    advisory_llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0.2
    )
    
    # Removed {context} from the prompt. Now it only relies on live data and general knowledge.
    advisory_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a live-market financial advisor. Use current market data and your broader financial knowledge to answer the user's query. Provide a concise, professional recommendation. Do not use markdown format."),
        ("human", "Query: {query}\nUser Profile: {profile}\nLive Market Data: {ticker} is trading at {price}")
    ])
    advisory_chain = advisory_prompt | advisory_llm
except Exception as e:
    logging.warning(f"Failed to init NVIDIA LLM: {e}")
    advisory_chain = None


def get_market_data(ticker: str) -> Dict:
    """Fetches real-time price using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            return {"ticker": ticker, "price": round(float(current_price), 2)}
        return {"ticker": ticker, "price": "N/A"}
    except Exception as e:
        logging.warning(f"yfinance failed for {ticker}: {e}")
        return {"ticker": ticker, "price": "N/A"}


def advisory_agent(state: Dict) -> Dict:
    """
    Financial Advisory Agent: 
    Provides insights using real-time Yahoo Finance data and LLM reasoning.
    """
    query = state.get("user_query", "")
    risk_profile = state.get("risk_profile", "moderate")
    market_ticker = state.get("market_ticker")
    
    reasons = []

    # 1. Fetch Real-time Market Data
    market_info = get_market_data(market_ticker) if market_ticker else {}
    m_price = market_info.get('price', "N/A")
    
    if market_ticker:
        reasons.append(f"Analyzed live market pricing for {market_ticker}")
    else:
        reasons.append("Providing general market strategy")

    # 2. LLM Inference
    if advisory_chain:
        try:
            profile_keys = ["credit_score", "income", "debt", "usual_location", "country", "amount"]
            profile_arr = [f"{k}: {state.get(k)}" for k in profile_keys if state.get(k) is not None]
            profile_str = ", ".join(profile_arr) if profile_arr else "No profile data provided"

            res = advisory_chain.invoke({
                "query": query,
                "profile": profile_str,
                "ticker": market_ticker or "None specified",
                "price": m_price
            })
            recommendation = res.content.strip()
        except Exception as e:
            logging.error(f"Advisory LLM failed: {e}")
            recommendation = f"Advisory LLM Error. Live Price: {m_price}"
    else:
        recommendation = "Advisory engine offline."
    
    return {
        "advisory_result": {
            "recommendation": recommendation,
            "market_data": market_info,
            "reasons": reasons
        }
    }