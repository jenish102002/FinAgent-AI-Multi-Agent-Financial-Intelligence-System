# agents/compliance_agent.py

import os
import logging
import pandas as pd
from typing import Dict
from difflib import SequenceMatcher

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate

logging.basicConfig(level=logging.INFO)

# ========================================================
# 1. Load Sanctions Data (OFAC SDN List)
# ========================================================
try:
    sanctions_df = pd.read_csv("data/ofac_sdn.csv")
    sanctions_names = set(sanctions_df["name"].str.lower())
    logging.info(f"OFAC SDN list loaded: {len(sanctions_names)} entries.")
except Exception:
    sanctions_names = set()
    logging.warning("OFAC SDN list not found. Sanctions screening disabled.")

# ========================================================
# 2. Regulatory Configuration
# ========================================================
# FATF High-Risk & Monitored Jurisdictions
HIGH_RISK_COUNTRIES = {"IR", "KP", "SY", "MM", "AF", "YE", "LY", "SO", "SD", "CU"}

# AML Thresholds (BSA/FinCEN)
AML_REPORTING_THRESHOLD = 10000     # CTR filing requirement
AML_HIGH_VALUE_THRESHOLD = 100000   # Enhanced Due Diligence trigger

# PEP (Politically Exposed Person) risk keywords
PEP_KEYWORDS = {"minister", "president", "governor", "senator", "general", "ambassador", "director"}

# ========================================================
# 3. Initialize LLM for Compliance Reporting
# ========================================================
try:
    compliance_llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0
    )

    compliance_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior compliance officer specializing in AML, KYC, and OFAC enforcement.
        You have been given the results of a multi-layer compliance screening.
        Write a professional compliance report summarizing the findings.
        
        Rules:
        - Cite specific regulations triggered (e.g., BSA Section 5313, OFAC SDN List, FATF guidelines).
        - If any check failed, clearly state the transaction must be BLOCKED and escalated.
        - If passed, confirm regulatory clearance with a brief summary.
        - Keep the report under 120 words.
        - Do not use markdown formatting."""),
        ("human", """Multi-Layer Compliance Screening Report:

Overall Status: {status}
Risk Level: {risk_level}
Triggered Flags: {flags}

Screening Details:
- OFAC SDN Match: {ofac_status}
- Fuzzy Name Match Score: {fuzzy_score}%
- AML Threshold Check: {aml_status}
- FATF Country Risk: {country_status}
- Transaction Amount: ${amount}
- Country: {country}
- User: {user_name}

Write your compliance assessment:""")
    ])

    compliance_chain = compliance_prompt | compliance_llm
except Exception as e:
    logging.warning(f"Failed to initialize Compliance LLM: {e}")
    compliance_chain = None


# ========================================================
# 4. Helper: Fuzzy Name Matching Against Sanctions List
# ========================================================
def fuzzy_sanctions_check(name: str, threshold: float = 0.80) -> dict:
    """
    Performs fuzzy string matching against the OFAC sanctions list.
    This catches misspellings and name variations that exact matching misses.
    Returns the best match and similarity score.
    """
    if not name or not sanctions_names:
        return {"match": False, "best_match": None, "score": 0.0}

    best_score = 0.0
    best_name = None

    for sanctioned in sanctions_names:
        score = SequenceMatcher(None, name, sanctioned).ratio()
        if score > best_score:
            best_score = score
            best_name = sanctioned

    return {
        "match": best_score >= threshold,
        "best_match": best_name if best_score >= threshold else None,
        "score": round(best_score * 100, 1)
    }


# ========================================================
# 5. Compliance Agent (Multi-Layer Screening)
# ========================================================
from typing import Dict

def compliance_agent(state: Dict) -> Dict:
    """
    Multi-Layer Regulatory Compliance Agent:
    Layer 1: OFAC SDN Array Screening
    Layer 2: Dual Threshold AML Check
    Layer 3: FATF Country Check
    Layer 4: LLM Compliance Report Generation
    """
    user_name_raw = state.get("user_name", "")
    user_name = user_name_raw.lower().strip() if user_name_raw else ""

    country_raw = state.get("country", "")
    country = country_raw.upper().strip() if country_raw else ""

    amount = state.get("amount") or 0.0

    flags = []
    status = "passed"
    risk_level = "LOW"

    # ─────────────────────────────────────────────
    # Layer 1: OFAC SDN Sanctions Screening
    # ─────────────────────────────────────────────
    ofac_status = "Clear"

    # 1a. Exact Match
    if user_name in sanctions_names:
        status = "failed"
        risk_level = "CRITICAL"
        ofac_status = "EXACT MATCH"
        flags.append(f"OFAC SDN exact match: '{user_name_raw}'")
        logging.warning(f"CRITICAL: OFAC exact match found for '{user_name_raw}'")

    # 1b. Fuzzy Match (catches misspellings / variations)
    else:
        fuzzy_result = fuzzy_sanctions_check(user_name)
        if fuzzy_result["match"]:
            status = "review"
            risk_level = "HIGH"
            ofac_status = f"FUZZY MATCH ({fuzzy_result['score']}%)"
            flags.append(
                f"Potential OFAC match: '{fuzzy_result['best_match']}' "
                f"(similarity: {fuzzy_result['score']}%)"
            )
            logging.warning(f"Fuzzy OFAC match: {fuzzy_result}")

    fuzzy_score = fuzzy_sanctions_check(user_name)["score"] if user_name else 0

    # ─────────────────────────────────────────────
    # Layer 2: AML Transaction Threshold Analysis
    # ─────────────────────────────────────────────
    aml_status = "Clear"

    # 2a. Currency Transaction Report threshold (BSA $10,000)
    if amount > AML_REPORTING_THRESHOLD:
        aml_status = "CTR Required"
        flags.append(f"CTR filing required: ${amount:,.0f} exceeds $10,000 BSA threshold")
        if risk_level == "LOW":
            risk_level = "MEDIUM"

    # 2b. Enhanced Due Diligence threshold ($100,000)
    if amount > AML_HIGH_VALUE_THRESHOLD:
        aml_status = "EDD Required"
        flags.append(f"Enhanced Due Diligence triggered: ${amount:,.0f} exceeds $100,000")
        risk_level = "HIGH"

    # ─────────────────────────────────────────────
    # Layer 3: FATF High-Risk Jurisdiction Check
    # ─────────────────────────────────────────────
    country_status = "Clear"

    if country in HIGH_RISK_COUNTRIES:
        status = "failed"
        risk_level = "CRITICAL"
        country_status = f"FATF HIGH-RISK ({country})"
        flags.append(f"FATF high-risk jurisdiction: {country}")

    # ─────────────────────────────────────────────
    # Layer 4: LLM Compliance Report Generation
    # ─────────────────────────────────────────────
    analysis = "Compliance analysis engine offline."
    if compliance_chain:
        try:
            res = compliance_chain.invoke({
                "status": status.upper(),
                "risk_level": risk_level,
                "flags": ", ".join(flags) if flags else "All checks passed — no flags triggered",
                "ofac_status": ofac_status,
                "fuzzy_score": fuzzy_score,
                "aml_status": aml_status,
                "country_status": country_status,
                "amount": amount or "N/A",
                "country": country or "Not provided",
                "user_name": user_name_raw or "Not provided"
            })
            analysis = res.content.strip()
            logging.info("Compliance Agent LLM report generated successfully.")
        except Exception as e:
            logging.error(f"Compliance LLM report failed: {e}")
            analysis = (
                f"Automated screening complete. Status: {status.upper()}. "
                f"Risk: {risk_level}. Flags: {', '.join(flags) if flags else 'None'}."
            )

    return {
        "compliance_result": {
            "status": status,
            "risk_level": risk_level,
            "flags": flags,
            "screening": {
                "ofac": ofac_status,
                "aml": aml_status,
                "country": country_status,
                "fuzzy_score": fuzzy_score
            },
            "analysis": analysis
        }
    }