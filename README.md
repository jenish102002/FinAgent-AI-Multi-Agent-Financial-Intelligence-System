<![CDATA[<h1 align="center">FinAgent AI</h1>
<h3 align="center">Multi-Agent Financial Intelligence System</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/LangGraph-FF6B6B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white"/>
  <img src="https://img.shields.io/badge/FAISS-0066CC?style=for-the-badge"/>
</p>

<p align="center">
  A production-grade AI system that orchestrates <b>Fraud Detection</b>, <b>Credit Risk Analysis</b>, <b>AML/KYC Compliance</b>, and <b>Financial Advisory</b> agents — running in parallel via LangGraph, powered by NVIDIA NIM inference.
</p>

<p align="center">
  <a href="#-architecture">Architecture</a> · <a href="#-features">Features</a> · <a href="#-tech-stack">Tech Stack</a> · <a href="#-quick-start">Quick Start</a> · <a href="#-api-reference">API Reference</a>
</p>

---

## The Problem

Financial institutions evaluate transactions through siloed systems — fraud checks in one tool, credit scoring in another, compliance in a third. Each system returns a partial picture. Analysts must manually synthesize results, introducing latency and human error into time-sensitive decisions.

## The Solution

**FinAgent AI** unifies four specialized AI agents under a single LangGraph orchestrator. A natural language query triggers parallel agent execution, and a deterministic consolidation engine synthesizes a single verdict — **APPROVAL**, **REVIEW**, or **ALERT** — with full explainability.

```
Input:  "I want to invest $200,000 in NVDA stock from Mumbai with $10K in existing debt"
Output: REVIEW — High transaction amount relative to average spending pattern
        ├─ Fraud Agent     → Score: 45/100, Flag: CLEAR
        ├─ Risk Agent      → Score: 30/100, Eligible: YES
        ├─ Compliance      → OFAC: Clear, AML: Clear, FATF: Clear
        └─ Advisory Agent  → NVDA @ $135.50, Moderate buy signal
```

---

## 🏗 Architecture

### System Design

```
                              ┌──────────────────────────┐
                              │      React Frontend      │
                              │    (Intelligence Console) │
                              └────────────┬─────────────┘
                                           │ POST /evaluate
                                           ▼
                              ┌──────────────────────────┐
                              │    FastAPI Gateway        │
                              │    (main.py)              │
                              └────────────┬─────────────┘
                                           │
                              ┌────────────▼─────────────┐
                              │    Intent Parser          │
                              │    LLaMA 3.1 via NIM      │
                              │                          │
                              │  Extracts: intent,       │
                              │  entities, risk signals  │
                              └────────────┬─────────────┘
                                           │
                              ┌────────────▼─────────────┐
                              │    Task Planner           │
                              │    (LangGraph Router)     │
                              └──┬──────┬──────┬──────┬──┘
                                 │      │      │      │
                    ┌────────────▼┐ ┌───▼────┐ ┌▼─────┐ ┌▼──────────┐
                    │   Fraud     │ │ Credit │ │ AML/ │ │ Financial │
                    │  Detection  │ │  Risk  │ │ KYC  │ │ Advisory  │
                    │             │ │        │ │      │ │ (RAG)     │
                    └──────┬──────┘ └───┬────┘ └┬─────┘ └┬──────────┘
                           │            │       │        │
                           └────────┬───┘───────┘────────┘
                                    │
                           ┌────────▼────────┐
                           │  Aggregator     │
                           │  (Consolidation │
                           │   Engine)       │
                           └────────┬────────┘
                                    │
                                    ▼
                        APPROVAL / REVIEW / ALERT
```

### Why These Design Decisions?

| Decision | Rationale |
|---|---|
| **LangGraph over LangChain Agents** | Deterministic graph execution with parallel edges — no unpredictable agent loops |
| **TypedDict over Pydantic** | Zero serialization overhead in the hot path; LangGraph natively consumes TypedDicts |
| **Parallel agent execution** | Agents share no dependencies — fraud, risk, compliance, advisory run simultaneously |
| **Rule-based aggregation** | Final verdicts must be explainable and auditable — no LLM in the decision layer |
| **FAISS + yFinance for RAG** | Combines static financial knowledge with real-time market data for grounded advisory |

---

## ✨ Features

### Intelligence Agents

| Agent | Capabilities |
|---|---|
| **Fraud Detection** | Behavioral velocity analysis, geo-anomaly detection, spending pattern deviation scoring, LLM-generated risk narrative |
| **Credit Risk** | Debt-to-income evaluation, credit score weighting, structured eligibility determination with explainable factors |
| **AML/KYC Compliance** | OFAC SDN sanctions screening, Levenshtein fuzzy name matching, BSA/FinCEN AML thresholds ($10K CTR, $100K EDD), FATF high-risk jurisdiction flagging |
| **Financial Advisory** | FAISS vector retrieval over financial knowledge base, yFinance real-time market data, LLM-synthesized investment recommendations |

### System Capabilities

- **Intent Classification** — LLaMA 3.1 extracts intent (`loan_approval`, `fraud_check`, `investment_query`, `compliance_check`, `general`) and entities from natural language
- **Dynamic Agent Routing** — Task planner selects only relevant agents per query (e.g., loan queries skip advisory)
- **Deterministic Verdicts** — Rule-based consolidation: any fraud flag → ALERT, any risk denial → REVIEW, all clear → APPROVAL
- **Full Explainability** — Every verdict includes a reasons array tracing exactly which agent triggered which signal

---

## 🛠 Tech Stack

### Backend

| Technology | Role |
|---|---|
| Python 3.10+ | Core runtime |
| FastAPI + Uvicorn | Async REST API with CORS |
| LangGraph | Cyclic graph orchestration with parallel edges |
| NVIDIA NIM (LLaMA 3.1 8B) | LLM inference — intent parsing, agent analysis |
| FAISS | Vector similarity search for RAG retrieval |
| yFinance | Real-time stock market data |
| LangChain | Prompt templates and LLM integration layer |

### Frontend

| Technology | Role |
|---|---|
| React 18 + Vite | Component-based UI with HMR |
| Vanilla CSS | Custom design system — no framework dependency |
| Axios | HTTP client for API communication |

---

## 📂 Project Structure

```
FinAgent-AI/
│
├── finagent/                            # Backend — FastAPI + LangGraph
│   ├── main.py                          # POST /evaluate endpoint, CORS config
│   ├── state.py                         # GraphState TypedDict definition
│   ├── graph.py                         # LangGraph compiled graph with parallel edges
│   │
│   ├── orchestrator/
│   │   ├── intent_parser.py             # LLM-based intent + entity extraction
│   │   ├── task_planner.py              # Dynamic agent selection logic
│   │   └── aggregator.py               # Rule-based verdict consolidation engine
│   │
│   ├── agents/
│   │   ├── fraud_agent.py               # Behavioral fraud detection + LLM analysis
│   │   ├── risk_agent.py                # Credit risk scoring + eligibility
│   │   ├── compliance_agent.py          # OFAC/AML/FATF multi-layer screening
│   │   └── advisory_agent.py            # RAG retrieval + yFinance + LLM advisory
│   │
│   ├── data/
│   │   ├── ofac_sdn.csv                 # OFAC Specially Designated Nationals list
│   │   └── finance_docs.txt             # RAG knowledge base documents
│   │
│   └── .env                             # NVIDIA_API_KEY configuration
│
├── finagent-ui/                         # Frontend — React + Vite
│   ├── index.html                       # Entry point with font imports
│   ├── vite.config.js                   # Vite build configuration
│   └── src/
│       ├── main.jsx                     # React DOM mount
│       ├── App.jsx                      # Root component
│       ├── index.css                    # Design system (tokens, layout, components)
│       │
│       ├── pages/
│       │   └── Home.jsx                 # Main dashboard — state management, layout
│       │
│       ├── features/
│       │   ├── InputPanel.jsx           # Query console with all GraphState fields
│       │   ├── DecisionPanel.jsx        # Verdict display (APPROVAL/REVIEW/ALERT)
│       │   ├── AgentPanel.jsx           # Fraud, Risk, Advisory agent cards
│       │   ├── CompliancePanel.jsx      # AML/KYC screening table with flags
│       │   └── ExplainPanel.jsx         # Timeline-based audit trail
│       │
│       └── services/
│           └── api.js                   # Axios client — POST /evaluate
│
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| NVIDIA NIM API Key | [Get free key →](https://build.nvidia.com) |

### 1. Clone

```bash
git clone https://github.com/jenish102002/FinAgent-AI-Multi-Agent-Financial-Intelligence-System.git
cd FinAgent-AI-Multi-Agent-Financial-Intelligence-System
```

### 2. Backend Setup

```bash
cd finagent

# Create virtual environment
python -m venv finagent_env
source finagent_env/bin/activate       # Windows: finagent_env\Scripts\activate

# Install dependencies
pip install fastapi uvicorn langchain langchain-core langchain-community \
    langchain-nvidia-ai-endpoints pydantic yfinance faiss-cpu pandas python-dotenv
```

### 3. Configure API Key

```bash
echo "NVIDIA_API_KEY=nvapi-your-key-here" > .env
```

### 4. Start Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://127.0.0.1:8000` — Swagger docs at `/docs`

### 5. Start Frontend

```bash
cd ../finagent-ui
npm install
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## 📡 API Reference

### `POST /evaluate`

Accepts a `GraphState`-compatible JSON body. All fields except `user_query` are optional — agents use defaults or skip if data is missing.

**Request:**
```json
{
  "user_query": "I want to apply for a $50,000 personal loan with my salary of $90,000",
  "user_name": "Jenish Patel",
  "credit_score": 720,
  "income": 90000,
  "debt": 15000,
  "risk_profile": "moderate",
  "amount": 50000,
  "avg_amount": 2000,
  "frequency": 3,
  "usual_frequency": 1,
  "location": "Mumbai",
  "usual_location": "New York",
  "country": "US",
  "market_ticker": "NVDA"
}
```

**Response:**
```json
{
  "status": "success",
  "intent": "loan_approval",
  "final_decision": {
    "decision": "APPROVAL",
    "reasons": [],
    "details": {
      "fraud": {
        "score": 15,
        "flag": false,
        "reasons": [],
        "analysis": "Transaction patterns are consistent with normal behavior..."
      },
      "risk": {
        "score": 22,
        "eligible": true,
        "reasons": [],
        "analysis": "Debt-to-income ratio of 16.7% is within acceptable range..."
      },
      "compliance": {
        "status": "passed",
        "risk_level": "LOW",
        "screening": {
          "ofac": "Clear",
          "fuzzy_score": 0,
          "aml": "Clear",
          "country": "Clear"
        },
        "flags": [],
        "analysis": "No sanctions matches found. Transaction complies with regulations..."
      },
      "advisory": {
        "recommendation": "Based on market analysis, NVDA is showing...",
        "market_data": {
          "ticker": "NVDA",
          "price": 135.50
        },
        "reasons": ["Strong quarterly earnings", "Positive analyst consensus"]
      }
    }
  }
}
```

### Intent Types

| Intent | Triggers |
|---|---|
| `loan_approval` | Loan, mortgage, credit applications |
| `fraud_check` | Suspicious transfers, velocity anomalies |
| `investment_query` | Stock analysis, portfolio questions |
| `compliance_check` | KYC verification, sanctions screening |
| `general` | Unclassified financial queries |

---

## 🧪 Test Scenarios

| Query | Expected Verdict | Key Signals |
|---|---|---|
| "Transfer $50,000 to an overseas account urgently from 3 different locations" | **ALERT** | Fraud: geo-anomaly + velocity spike |
| "Should I invest $5,000 in Apple stock with no existing debt?" | **APPROVAL** | All agents clear, positive advisory |
| "I need a $100,000 loan but have $80,000 in credit card debt" | **REVIEW** | Risk: debt-to-income ratio exceeded |
| "Send $150,000 to Iran immediately" | **ALERT** | Compliance: FATF high-risk jurisdiction + AML threshold |

---

## 🗺 Roadmap

- [ ] Cloud deployment — Render (backend) + Vercel (frontend)
- [ ] JWT authentication and user sessions
- [ ] Live news sentiment analysis agent
- [ ] Portfolio tracking dashboard
- [ ] Multi-turn conversational memory
- [ ] WebSocket streaming for real-time agent status

---

## 👤 Author

**Jenish Jagdishkumar Patel**
GRC Intern @ Intel Corporation · M.Tech CS @ SVNIT · Ex-ISRO Intern

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/jenish102002)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jenish102002)

---

<p align="center">
  If this project was useful, consider giving it a ⭐ — it helps others discover it.
</p>
]]>