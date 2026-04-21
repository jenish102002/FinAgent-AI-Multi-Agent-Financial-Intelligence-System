# FinAgent AI 🧠💹
### Multi-Agent Financial Intelligence System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/LangGraph-FF6B6B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white"/>
  <img src="https://img.shields.io/badge/FAISS-0066CC?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/LLaMA_3.1_8B-FF6600?style=for-the-badge"/>
</p>

<p align="center">
  <b>A production-grade AI system that orchestrates Fraud Detection, Credit Risk Analysis, AML/KYC Compliance, and Financial Advisory agents — running in parallel via LangGraph, powered by NVIDIA NIM inference.</b>
</p>

<p align="center">
  <a href="#-the-problem">Problem</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-api-reference">API</a> •
  <a href="#-test-scenarios">Test Scenarios</a>
</p>

---

## ⚡ See It In Action

**Input:**
```
"I want to invest $200,000 in NVDA stock from Mumbai with $10K in existing debt"
```

**Output in < 3 seconds:**
```
Final Decision: REVIEW
├─ 🛡️ Fraud Agent    → Score: 45/100  | Flag: CLEAR
├─ 📊 Risk Agent     → Score: 30/100  | Eligible: YES
├─ ⚖️ Compliance     → OFAC: Clear   | AML: Clear | FATF: Clear
└─ 📈 Advisory       → NVDA @ $135.50 | Moderate buy signal
```

---

## 🎯 The Problem

Financial institutions evaluate transactions through **siloed systems** — fraud checks in one tool, credit scoring in another, compliance in a third. Each returns a partial picture. Analysts must manually synthesize results, introducing latency and human error into time-sensitive decisions.

## ✅ The Solution

FinAgent AI unifies **four specialized AI agents** under a single LangGraph orchestrator. A natural language query triggers **parallel agent execution**, and a deterministic consolidation engine synthesizes a single verdict — **APPROVAL**, **REVIEW**, or **ALERT** — with full explainability and audit trail.

---

## 🏗️ Architecture

### System Design

```
┌──────────────────────────┐
│      React Frontend      │
│   (Intelligence Console) │
└────────────┬─────────────┘
             │  POST /evaluate
             ▼
┌──────────────────────────┐
│     FastAPI Gateway      │
│        (main.py)         │
└────────────┬─────────────┘
             │
┌────────────▼─────────────┐
│      Intent Parser       │
│   LLaMA 3.1 via NIM      │
│  Extracts: intent,       │
│  entities, risk signals  │
└────────────┬─────────────┘
             │
┌────────────▼─────────────┐
│      Task Planner        │
│   (LangGraph Router)     │
└──┬──────┬──────┬──────┬──┘
   │      │      │      │   ← Parallel execution
   ▼      ▼      ▼      ▼
┌──────┐ ┌─────┐ ┌─────┐ ┌──────────┐
│Fraud │ │Risk │ │AML/ │ │Financial │
│Agent │ │Agent│ │KYC  │ │Advisory  │
│      │ │     │ │     │ │  (RAG)   │
└──┬───┘ └──┬──┘ └──┬──┘ └────┬─────┘
   └────────┴────────┴─────────┘
                    │
        ┌───────────▼──────────┐
        │      Aggregator      │
        │  (Rule-based Engine) │
        └───────────┬──────────┘
                    │
                    ▼
         APPROVAL / REVIEW / ALERT
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| **LangGraph over LangChain Agents** | Deterministic graph execution with parallel edges — no unpredictable agent loops |
| **TypedDict over Pydantic** | Zero serialization overhead in the hot path; LangGraph natively consumes TypedDicts |
| **Parallel agent execution** | Agents share no dependencies — all four run simultaneously |
| **Rule-based aggregation** | Final verdicts must be explainable and auditable — no LLM in the decision layer |
| **FAISS + yFinance for RAG** | Combines static financial knowledge with real-time market data for grounded advisory |

---

## ✨ Features

### Intelligence Agents

| Agent | Capabilities |
|---|---|
| 🛡️ **Fraud Detection** | Behavioral velocity analysis, geo-anomaly detection, spending pattern deviation scoring, LLM-generated risk narrative |
| 📊 **Credit Risk** | Debt-to-income evaluation, credit score weighting, structured eligibility determination with explainable factors |
| ⚖️ **AML/KYC Compliance** | OFAC SDN sanctions screening, Levenshtein fuzzy name matching, BSA/FinCEN AML thresholds ($10K CTR, $100K EDD), FATF high-risk jurisdiction flagging |
| 📈 **Financial Advisory** | FAISS vector retrieval over financial knowledge base, yFinance real-time market data, LLM-synthesized investment recommendations |

### System Capabilities

- **Intent Classification** — LLaMA 3.1 extracts intent (`loan_approval`, `fraud_check`, `investment_query`, `compliance_check`, `general`) and entities from natural language
- **Dynamic Agent Routing** — Task planner selects only relevant agents per query
- **Deterministic Verdicts** — Any fraud flag → ALERT | Any risk denial → REVIEW | All clear → APPROVAL
- **Full Explainability** — Every verdict includes a `reasons` array tracing which agent triggered which signal
- **Swagger Docs** — Auto-generated API documentation at `/docs`

---

## 🛠️ Tech Stack

### Backend
| Technology | Role |
|---|---|
| Python 3.10+ | Core runtime |
| FastAPI + Uvicorn | Async REST API with CORS |
| LangGraph | Cyclic graph orchestration with parallel edges |
| NVIDIA NIM — LLaMA 3.1 8B | LLM inference for intent parsing and agent analysis |
| FAISS | Vector similarity search for RAG retrieval |
| yFinance | Real-time stock market data pipeline |
| LangChain | Prompt templates and LLM integration layer |

### Frontend
| Technology | Role |
|---|---|
| React 18 + Vite | Component-based UI with HMR |
| Vanilla CSS | Custom glassmorphism design system — no framework dependency |
| Axios | HTTP client for API communication |

---

## 📂 Project Structure

```
FinAgent-AI/
│
├── finagent/                        # ⚙️ Backend — FastAPI + LangGraph
│   ├── main.py                      # POST /evaluate endpoint, CORS config
│   ├── state.py                     # GraphState TypedDict definition
│   ├── graph.py                     # LangGraph compiled graph with parallel edges
│   │
│   ├── orchestrator/
│   │   ├── intent_parser.py         # LLM-based intent + entity extraction
│   │   ├── task_planner.py          # Dynamic agent selection logic
│   │   └── aggregator.py            # Rule-based verdict consolidation engine
│   │
│   ├── agents/
│   │   ├── fraud_agent.py           # Behavioral fraud detection + LLM analysis
│   │   ├── risk_agent.py            # Credit risk scoring + eligibility
│   │   ├── compliance_agent.py      # OFAC/AML/FATF multi-layer screening
│   │   └── advisory_agent.py        # RAG retrieval + yFinance + LLM advisory
│   │
│   ├── data/
│   │   ├── ofac_sdn.csv             # OFAC Specially Designated Nationals list
│   │   └── finance_docs.txt         # RAG knowledge base documents
│   │
│   └── .env                         # NVIDIA_API_KEY configuration
│
└── finagent-ui/                     # 🖥️ Frontend — React + Vite
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css                # Design system (tokens, layout, keyframes)
        │
        ├── pages/
        │   └── Home.jsx             # Main dashboard — state management
        │
        ├── features/
        │   ├── InputPanel.jsx       # Query console with all GraphState fields
        │   ├── DecisionPanel.jsx    # Verdict display (APPROVAL/REVIEW/ALERT)
        │   ├── AgentPanel.jsx       # Fraud, Risk, Advisory agent cards
        │   ├── CompliancePanel.jsx  # AML/KYC screening table with flags
        │   └── ExplainPanel.jsx     # Timeline-based audit trail
        │
        └── services/
            └── api.js               # Axios client — POST /evaluate
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| NVIDIA NIM API Key | [Get free key →](https://build.nvidia.com) |

### 1. Clone the Repository
```bash
git clone https://github.com/jenish102002/FinAgent-AI-Multi-Agent-Financial-Intelligence-System.git
cd FinAgent-AI-Multi-Agent-Financial-Intelligence-System
```

### 2. Backend Setup
```bash
cd finagent
python -m venv finagent_env
source finagent_env/bin/activate       # Windows: finagent_env\Scripts\activate

pip install fastapi uvicorn langchain langchain-core langchain-community \
    langchain-nvidia-ai-endpoints pydantic yfinance faiss-cpu pandas python-dotenv
```

### 3. Configure API Key
```bash
# Create .env inside /finagent
echo "NVIDIA_API_KEY=nvapi-your-key-here" > .env
```

### 4. Initialize Data Files
- Place `ofac_sdn.csv` in `finagent/data/` for OFAC sanctions testing
- Place `finance_docs.txt` in `finagent/data/` for RAG embeddings

### 5. Start the Backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
> API live at `http://127.0.0.1:8000` · Swagger docs at `http://127.0.0.1:8000/docs`

### 6. Start the Frontend
```bash
cd ../finagent-ui
npm install
npm run dev
```
> UI live at `http://localhost:5173`

---

## 📡 API Reference

### `POST /evaluate`

All fields except `user_query` are optional — agents use defaults or skip if data is missing.

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
      "fraud":      { "score": 15,  "flag": false,    "analysis": "Transaction patterns consistent with normal behavior..." },
      "risk":       { "score": 22,  "eligible": true,  "analysis": "Debt-to-income ratio of 16.7% within acceptable range..." },
      "compliance": { "status": "passed", "risk_level": "LOW", "ofac": "Clear", "aml": "Clear" },
      "advisory":   { "recommendation": "NVDA showing bullish momentum...", "price": 135.50 }
    }
  }
}
```

### Intent Types

| Intent | Triggered By |
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
| "Transfer $50,000 to an overseas account urgently from 3 different locations" | 🚨 **ALERT** | Fraud: geo-anomaly + velocity spike |
| "Should I invest $5,000 in Apple stock with no existing debt?" | ✅ **APPROVAL** | All agents clear, positive advisory |
| "I need a $100,000 loan but have $80,000 in credit card debt" | 🔁 **REVIEW** | Risk: debt-to-income ratio exceeded |
| "Send $150,000 to Iran immediately" | 🚨 **ALERT** | Compliance: FATF high-risk jurisdiction + AML threshold |

---

## 🗺️ Roadmap

- [ ] Deploy on Render (backend) + Vercel (frontend) with live demo link
- [ ] JWT authentication and user sessions
- [ ] Live news sentiment analysis agent
- [ ] Portfolio tracking dashboard
- [ ] Multi-turn conversational memory
- [ ] WebSocket streaming for real-time agent status updates

---

## 👨‍💻 Author

**Jenish Jagdishkumar Patel**
GRC Intern @ Intel Corporation · M.Tech CS @ SVNIT · Ex-ISRO Intern

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/jenish102002)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jenish102002)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://your-portfolio-link-here)

---

<p align="center">
  If this project was useful, consider giving it a ⭐ — it helps others discover it.
  <br><br>
  Built with ❤️ by Jenish Patel · Open to SDE / GenAI Roles
</p>