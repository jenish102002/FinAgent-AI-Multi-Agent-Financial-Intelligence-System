def aggregator(state: dict):
    fraud = state.get("fraud_result") or {"status": "not_run"}
    risk = state.get("risk_result") or {"status": "not_run"}
    compliance = state.get("compliance_result") or {"status": "not_run"}
    advisory = state.get("advisory_result") or {"status": "not_run"}

    decision = "APPROVAL"
    reasons = []

    # 🚨 Fraud has highest priority
    if fraud.get("flag"):
        decision = "ALERT"
        reasons.append("High fraud risk detected")

    # ⚖️ Compliance check
    elif compliance.get("status") not in ["passed", "not_run"]:
        decision = "ALERT"
        reasons.append("Compliance check failed")

    # 📊 Risk evaluation
    elif risk.get("status") != "not_run" and not risk.get("eligible", True):
        decision = "REVIEW"
        reasons.append("Risk score too high")

    return {
        **state,
        "final_decision": {
            "decision": decision,
            "reasons": reasons,
            "details": {
                "fraud": fraud,
                "risk": risk,
                "compliance": compliance,
                "advisory": advisory
            }
        }
    }