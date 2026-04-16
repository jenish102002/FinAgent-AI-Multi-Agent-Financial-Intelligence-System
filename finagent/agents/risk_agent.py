# agents/risk_agent.py

import os
import logging
from typing import Dict

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate

logging.basicConfig(level=logging.INFO)

# --- Initialize NVIDIA LLM for Risk Assessment ---
try:
    risk_llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0
    )

    risk_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior credit risk analyst at a financial institution.
        You have been given the results of an automated credit risk assessment.
        Your job is to write a concise, professional credit risk report.
        
        Rules:
        - Explain how the credit score and debt-to-income ratio affect eligibility.
        - If the applicant is ineligible, explain why clearly and suggest improvement steps.
        - If eligible, confirm their financial health and note any mild concerns.
        - Keep the analysis under 100 words.
        - Do not use markdown formatting."""),
        ("human", """Credit Risk Assessment Results:
Risk Score: {risk_score}/100
Eligible: {eligible}
Triggered Reasons: {reasons}

Applicant Financial Profile:
- Credit Score: {credit_score}
- Annual Income: ${income}
- Total Debt: ${debt}
- Debt-to-Income Ratio: {dti}%

Write your credit risk assessment report:""")
    ])

    risk_chain = risk_prompt | risk_llm
except Exception as e:
    logging.warning(f"Failed to initialize Risk LLM: {e}")
    risk_chain = None


def risk_agent(state: Dict) -> Dict:
    """
    Hybrid Credit Risk Agent:
    1. Deterministic calculation of debt-to-income and credit minimums.
    2. LLM analysis for personalized credit reporting.
    """
    
    credit_score = state.get("credit_score") or 0
    debt = state.get("debt") or 0.0
    income = state.get("income") or 0.0

    reasons = []
    risk_score = 0

    # 1. Credit Score Check
    if credit_score < 600:
        risk_score += 40
        reasons.append("Low credit score")
    elif credit_score <= 700:
        risk_score += 20
        reasons.append("Fair credit score")

    # 2. Debt-to-Income Ratio (DTI)
    dti = round((debt / (income + 1)) * 100, 2)
    if dti > 40:
        risk_score += 40
        reasons.append("High debt-to-income ratio (>40%)")
    elif dti > 30:
        risk_score += 20
        reasons.append("Elevated debt-to-income ratio (>30%)")

    risk_score = min(risk_score, 100)
    eligible = risk_score < 50

    # --- LLM Analysis Layer ---
    analysis = "Risk analysis engine offline."
    if risk_chain:
        try:
            res = risk_chain.invoke({
                "risk_score": risk_score,
                "eligible": "YES" if eligible else "NO",
                "reasons": ", ".join(reasons) if reasons else "No risk flags triggered",
                "credit_score": credit_score or "Not provided",
                "income": income or "Not provided",
                "debt": debt or "Not provided",
                "dti": dti
            })
            analysis = res.content.strip()
            logging.info("Risk Agent LLM analysis generated successfully.")
        except Exception as e:
            logging.error(f"Risk LLM analysis failed: {e}")
            analysis = f"Automated assessment complete. Risk Score: {risk_score}/100. Eligible: {'Yes' if eligible else 'No'}."

    return {
        "risk_result": {
            "score": risk_score,
            "eligible": eligible,
            "reasons": reasons,
            "analysis": analysis
        }
    }