# agents/fraud_agent.py

import os
import logging
from typing import Dict

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate

logging.basicConfig(level=logging.INFO)

# --- Initialize NVIDIA LLM for Fraud Analysis ---
try:
    fraud_llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0
    )

    fraud_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior fraud analyst at a financial institution.
        You have been given the results of an automated behavioral fraud detection scan.
        Your job is to write a concise, professional fraud analysis report.
        
        Rules:
        - Explain each triggered flag in plain language.
        - If the risk score is high (>=50), recommend immediate transaction hold.
        - If the risk score is low (<50), confirm the transaction appears legitimate.
        - Keep the analysis under 100 words.
        - Do not use markdown formatting."""),
        ("human", """Transaction Fraud Scan Results:
Risk Score: {risk_score}/100
Fraud Flagged: {flag}
Triggered Reasons: {reasons}

Transaction Context:
- Amount: ${amount} (User Average: ${avg_amount})
- Location: {location} (Usual: {usual_location})
- Frequency: {frequency} txns/hr (Usual: {usual_frequency} txns/hr)

Write your fraud analysis report:""")
    ])

    fraud_chain = fraud_prompt | fraud_llm
except Exception as e:
    logging.warning(f"Failed to initialize Fraud LLM: {e}")
    fraud_chain = None


def fraud_agent(state: Dict) -> Dict:
    """
    Hybrid Fraud Detection Agent:
    1. Deterministic behavioral rules for accurate scoring
    2. LLM-powered analysis for explainable reporting
    """

    amount = state.get("amount", 0)
    avg_amount = state.get("avg_amount", 0)

    frequency = state.get("frequency", 0)  # txns per hour
    usual_frequency = state.get("usual_frequency", 0)

    location = state.get("location", "")
    usual_location = state.get("usual_location", "")

    risk_score = 0
    reasons = []

    # 🚨 1. Velocity Check
    if frequency > usual_frequency * 2:
        risk_score += 30
        reasons.append("High transaction velocity")

    # 🌍 2. Geo Anomaly
    if location and usual_location and location != usual_location:
        risk_score += 30
        reasons.append("Unusual location detected")

    # 💰 3. Spending Pattern
    if amount and avg_amount and amount > avg_amount * 3:
        risk_score += 40
        reasons.append("Unusual high spending")

    # Normalize score
    risk_score = min(risk_score, 100)
    flag = True if risk_score >= 50 else False

    # --- LLM Analysis Layer ---
    analysis = "Fraud analysis engine offline."
    if fraud_chain:
        try:
            res = fraud_chain.invoke({
                "risk_score": risk_score,
                "flag": "YES" if flag else "NO",
                "reasons": ", ".join(reasons) if reasons else "None triggered",
                "amount": amount or "N/A",
                "avg_amount": avg_amount or "N/A",
                "location": location or "N/A",
                "usual_location": usual_location or "N/A",
                "frequency": frequency or "N/A",
                "usual_frequency": usual_frequency or "N/A"
            })
            analysis = res.content.strip()
            logging.info(f"Fraud Agent LLM analysis generated successfully.")
        except Exception as e:
            logging.error(f"Fraud LLM analysis failed: {e}")
            analysis = f"Automated scan complete. Risk Score: {risk_score}/100. Flags: {', '.join(reasons) if reasons else 'None'}."

    return {
        "fraud_result": {
            "score": risk_score,
            "flag": flag,
            "reasons": reasons,
            "analysis": analysis
        }
    }