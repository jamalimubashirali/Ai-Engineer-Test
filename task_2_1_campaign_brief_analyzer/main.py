"""
main.py — FastAPI application entry-point for Task 2.1.

Run with:
    uvicorn main:app --reload
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="AI Campaign Brief Analyzer",
    description="Submit a campaign brief (plain text or PDF) and receive a structured AI analysis.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
