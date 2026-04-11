# agents/fraud_agent.py

from typing import Dict


def fraud_agent(state: Dict) -> Dict:
    """
    Behavioral Fraud Detection (Explainable)
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
    if location != usual_location:
        risk_score += 30
        reasons.append("Unusual location detected")

    # 💰 3. Spending Pattern
    if amount > avg_amount * 3:
        risk_score += 40
        reasons.append("Unusual high spending")

    # Normalize score
    risk_score = min(risk_score, 100)

    flag = True if risk_score >= 50 else False

    return {
        "fraud_result": {
            "score": risk_score,
            "flag": flag,
            "reasons": reasons
        }
    }