# agents/risk_agent.py
from typing import Dict

def risk_agent(state: Dict) -> Dict:
    """
    Credit Risk Assessment
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
    dti = debt / (income + 1)
    if dti > 0.4:
        risk_score += 40
        reasons.append("High debt-to-income ratio (>40%)")
    elif dti > 0.3:
        risk_score += 20
        reasons.append("Elevated debt-to-income ratio (>30%)")
        
    risk_score = min(risk_score, 100)
    eligible = risk_score < 50
    
    return {
        "risk_result": {
            "score": risk_score,
            "eligible": eligible,
            "reasons": reasons
        }
    }