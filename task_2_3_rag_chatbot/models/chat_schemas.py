"""
models/chat_schemas.py — Pydantic schemas for Task 2.3 RAG chatbot output.
"""
from pydantic import BaseModel, Field


class ChatAnswer(BaseModel):
    """Structured response from the RAG chatbot."""
    answer: str = Field(..., description="Factual answer sourced from the documents.")
    source: str = Field(..., description="Source document name the answer was drawn from.")
    quote: str = Field(..., description="Verbatim quote from the source that supports the answer.")
