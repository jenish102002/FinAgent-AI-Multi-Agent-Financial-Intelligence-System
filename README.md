# FinAgent AI 🧠💹
### Multi-Agent Financial Intelligence System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/LangGraph-FF6B6B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white"/>
  <img src="https://img.shields.io/badge/FAISS-0066CC?style=for-the-badge"/>
</p>

<p align="center">
  <b>An intelligent, production-grade AI system that autonomously orchestrates Fraud Detection, Credit Risk Analysis, Compliance Validation, and Financial Advisory — in parallel, in real-time.</b>
</p>

<p align="center">
  <a href="#-demo">View Demo</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a>
</p>

---

## 🎯 What is FinAgent AI?

FinAgent AI is a **Multi-Agent LLM System** built with **LangGraph** that routes a single user query through specialized AI agents simultaneously — delivering a consolidated financial decision in seconds.

**Example Query:**
> *"I want to invest $200,000 into NVDA stock immediately. Will this large transfer affect my mortgage application given my $10,000 credit card debt?"*

**FinAgent response in < 3 seconds:**
- 🛡️ Fraud Agent → **No anomaly detected** (behavioral pattern normal)
- 📊 Risk Agent → **REVIEW** (high exposure relative to debt ratio)
- ⚖️ Compliance Agent → **APPROVED** (no sanctions match)
- 📈 Advisory Agent → **NVDA current price: $XXX — moderate buy signal**
- 🧠 Final Verdict → **⚠️ REVIEW — High risk investment relative to liability**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Multi-Agent Orchestration** | LangGraph-powered parallel agent execution with dynamic routing based on user intent |
| 🛡️ **Behavioral Fraud Detection** | Velocity checks, geo-pattern analysis, spending limit anomalies with explainable AI scoring |
| 📊 **Credit Risk Evaluation** | Real-time financial exposure analysis with structured risk scoring |
| ⚖️ **AML/KYC Compliance** | OFAC sanctions list matching, KYC validation, and regulatory compliance checks |
| 📈 **RAG-Powered Advisory** | FAISS vector store + yFinance real-time data for personalized investment recommendations |
| ⚡ **LLM Orchestration Layer** | NVIDIA NIM (LLaMA 3.1 8B) for intent parsing and task planning |
| 🎨 **Professional Dashboard** | Clean React frontend with refined Vanilla CSS design system |

---

## 🏗️ Architecture

### Multi-Agent Workflow (LangGraph)

```
User Query (React UI)
        │
        ▼
  FastAPI Endpoint
        │
        ▼
  Intent Parser ──── LLaMA 3.1 (NVIDIA NIM)
        │
        ▼
  Task Planner (LangGraph Router)
        │
   ┌────┴────────────────────┐
   │         │               │              │
   ▼         ▼               ▼              ▼
Fraud     Credit Risk    Compliance    Advisory
Agent      Agent          Agent         Agent
   │         │               │              │
   └────┬────────────────────┘
        │
        ▼
  Consolidation Engine
        │
        ▼
  APPROVAL / REVIEW / ALERT
```

### Key Design Decisions
- **Parallel Execution** — All agents run simultaneously via LangGraph's cyclic graph, not sequentially
- **TypedDict State Schema** — Lightweight native Python memory management (no Pydantic overhead)
- **Deterministic Consolidation** — Rule-based final verdict engine ensures consistent, explainable outputs
- **RAG + Live Data** — FAISS embeddings combined with yFinance API for grounded, real-time advisory

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **FastAPI + Uvicorn** | Async REST API layer |
| **LangGraph** | Multi-agent orchestration with cyclic graph execution |
| **NVIDIA NIM — LLaMA 3.1 8B** | LLM inference for intent parsing and planning |
| **FAISS** | Vector database for RAG document retrieval |
| **yFinance** | Real-time financial market data |
| **LangChain** | LLM tooling and prompt management |

### Frontend
| Technology | Purpose |
|---|---|
| **React + Vite** | Fast, modular UI framework |
| **Vanilla CSS** | Professional dashboard design system |

---

## 📂 Project Structure

```
FinAgent-AI/
├── finagent/                        # FastAPI Backend
│   ├── agents/
│   │   ├── fraud_agent.py           # Behavioral fraud detection
│   │   ├── risk_agent.py            # Credit risk scoring
│   │   ├── compliance_agent.py      # AML/KYC/sanctions validation
│   │   └── advisory_agent.py        # RAG-powered financial advisory
│   ├── orchestrator/
│   │   ├── intent_parser.py         # LLM-based query understanding
│   │   ├── task_planner.py          # LangGraph routing logic
│   │   └── aggregator.py            # Multi-agent verdict consolidation
│   ├── data/
│   │   ├── ofac_sdn.csv             # Sanctions list for AML matching
│   │   └── finance_docs.txt         # RAG knowledge base
│   ├── graph.py                     # LangGraph parallel edge router
│   ├── state.py                     # TypedDict memory schema
│   └── main.py                      # FastAPI POST /evaluate endpoint
│
└── finagent-ui/                     # React Frontend
    └── src/
        ├── features/                # InputPanel, AgentPanel, DecisionPanel,
        │                            # CompliancePanel, ExplainPanel
        ├── services/                # API service layer (axios)
        ├── pages/                   # Home page with state management
        └── index.css                # Design system tokens and animations
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- NVIDIA NIM API Key → [Get free key here](https://build.nvidia.com)

### 1. Clone the Repository
```bash
git clone https://github.com/jenish102002/FinAgent-AI-Multi-Agent-Financial-Intelligence-System.git
cd FinAgent-AI-Multi-Agent-Financial-Intelligence-System
```

### 2. Backend Setup
```bash
cd finagent
python -m venv finagent_env
source finagent_env/bin/activate  # Windows: finagent_env\Scripts\activate

pip install fastapi uvicorn langchain langchain-core langchain-community \
    langchain-nvidia-ai-endpoints pydantic yfinance faiss-cpu pandas python-dotenv
```

### 3. Configure Environment Variables
```bash
# Create .env file inside /finagent
echo "NVIDIA_API_KEY=nvapi-your-key-here" > .env
```

### 4. Initialize Data Files
- Place `ofac_sdn.csv` in `finagent/data/` for AML sanctions testing
- Place `finance_docs.txt` in `finagent/data/` for RAG embeddings

### 5. Start the Backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
> API live at: `http://127.0.0.1:8000/evaluate`

### 6. Start the Frontend
```bash
cd ../finagent-ui
npm install
npm run dev
```
> UI live at: `http://localhost:5173`

---

## 📡 API Reference

### `POST /evaluate`

**Request Body (GraphState fields):**
```json
{
  "user_query": "I want to invest $200,000 in NVDA stock immediately",
  "user_name": "John Doe",
  "amount": 200000,
  "avg_amount": 5000,
  "frequency": 3,
  "usual_frequency": 1,
  "location": "Mumbai",
  "usual_location": "New York",
  "country": "US",
  "credit_score": 720,
  "income": 120000,
  "debt": 10000,
  "risk_profile": "moderate",
  "market_ticker": "NVDA"
}
```

**Response:**
```json
{
  "status": "success",
  "intent": "advisory",
  "final_decision": {
    "decision": "REVIEW",
    "reasons": ["High transaction amount relative to average"],
    "details": {
      "fraud": { "score": 30, "flag": false, "analysis": "..." },
      "risk": { "score": 20, "eligible": true, "analysis": "..." },
      "compliance": { "status": "passed", "risk_level": "LOW", "analysis": "..." },
      "advisory": { "recommendation": "...", "market_data": { "ticker": "NVDA", "price": 135.50 } }
    }
  }
}
```

---

## 🧪 Sample Queries to Try

```
"Transfer $50,000 to an overseas account urgently from 3 different locations"
→ Expected: 🚨 ALERT — High fraud probability (geo-anomaly + velocity)

"Should I invest $5,000 in Apple stock with no existing debt?"
→ Expected: ✅ APPROVAL — Low risk, positive advisory signal

"I need a $100,000 loan but have $80,000 in credit card debt"
→ Expected: 🔁 REVIEW — Credit risk threshold exceeded
```

---

## 🗺️ Roadmap

- [ ] Deploy on Render (Backend) + Vercel (Frontend)
- [ ] Add user authentication with JWT
- [ ] Integrate live news sentiment analysis agent
- [ ] Add portfolio tracking dashboard
- [ ] Support multi-turn conversation memory

---

## 👨‍💻 Author

**Jenish Jagdishkumar Patel**
GRC Intern @ Intel Corporation | M.Tech CS @ SVNIT | Ex-ISRO Intern

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/jenish102002)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jenish102002)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](your-portfolio-link-here)

---

## ⭐ Support

If you found this project useful or interesting, please consider giving it a **⭐ star** on GitHub — it helps other developers discover it!

---

<p align="center">Built with ❤️ by Jenish Patel | Open to SDE / GenAI Roles</p>