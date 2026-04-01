"""
models/brief_schemas.py — Pydantic schemas for Task 2.1 output parsing.
"""
from typing import List
from pydantic import BaseModel, Field


class BriefAnalysis(BaseModel):
    """Structured analysis of a campaign brief, returned by the LLM."""
    audience: str = Field(
        ..., description="Target audience persona (demographics + psychographics)."
    )
    key_messages: List[str] = Field(
        ..., description="Array of core messages / value propositions."
    )
    tone: str = Field(
        ..., description="Tone of voice for the campaign."
    )
    channels: List[str] = Field(
        ..., description="Suggested media / distribution channels."
    )
    risks: List[str] = Field(
        ..., description="Brand safety concerns or execution risk flags."
    )
