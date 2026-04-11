from dotenv import load_dotenv
load_dotenv() # Load keys for NVIDIA LLMs before import

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from state import AgentRequest
from typing import Optional
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

@app.post("/evaluate")
async def evaluate(request: AgentRequest):
    if graph is None:
        raise HTTPException(status_code=500, detail="Orchestration graph failed to initialize properly.")

    try:
        # Pydantic explicitly converts the LIVE incoming JSON payload into a dictionary here.
        # exclude_unset=True guarantees zero fallback defaults are sent downstream.
        input_data = request.model_dump(exclude_unset=True, exclude_none=True)
        result = await graph.ainvoke(input_data)
        
        return {
            "status": "success",
            "intent": result.get("intent", "unknown"),
            "final_decision": result.get("final_decision", {})
        }
    except Exception as e:
        logging.error(f"Execution Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))