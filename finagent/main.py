from dotenv import load_dotenv
load_dotenv() # Load keys for NVIDIA LLMs before import

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from graph import build_graph
import logging

app = FastAPI(
    title="FinAgent API",
    description="Multi-Agent Financial Intelligence System API connecting LangGraph & NVIDIA NIM",
    version="1.0.0"
)

# Crucial for Frontend communication (React/Vue/HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev. Restrict this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    graph = build_graph()
except Exception as e:
    logging.error(f"Failed to build graph: {e}")
    graph = None

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "FinAgent Multi-Agent Orchestrator is running."}

from typing import Dict, Any

@app.post("/evaluate")
async def evaluate(request: Dict[str, Any]):
    if graph is None:
        raise HTTPException(status_code=500, detail="Orchestration graph failed to initialize properly.")

    try:
        # Pass the raw dictionary directly into LangGraph
        result = await graph.ainvoke(request)
        
        return {
            "status": "success",
            "intent": result.get("intent", "unknown"),
            "final_decision": result.get("final_decision", {})
        }
    except Exception as e:
        logging.error(f"Execution Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))