# agents/compliance_agent.py

import pandas as pd
from typing import Dict

# 🔥 Load sanctions list once
try:
    sanctions_df = pd.read_csv("data/ofac_sdn.csv")
    sanctions_names = set(sanctions_df["name"].str.lower())
except:
    sanctions_names = set()


def compliance_agent(state: Dict) -> Dict:
    """
    AML + OFAC Compliance Check
    """

    user_name_raw = state.get("user_name")
    user_name = user_name_raw.lower() if user_name_raw else ""
    
    country_raw = state.get("country")
    country = country_raw.upper() if country_raw else ""
    
    amount = state.get("amount") or 0

    reasons = []
    status = "passed"

    # 🚫 1. Sanction List Check (OFAC)
    if user_name in sanctions_names:
        status = "failed"
        reasons.append("User found in OFAC sanctions list")

    # 💰 2. AML Rule (High Value Transaction)
    if amount > 100000:
        reasons.append("High-value transaction (AML threshold)")

    # 🌍 3. High-Risk Country (Example)
    high_risk_countries = ["IR", "KP", "SY"]

    if country in high_risk_countries:
        status = "failed"
        reasons.append("Transaction from high-risk country")

    return {
        "compliance_result": {
            "status": status,
            "reasons": reasons
        }
    }