"""
models/copy_schemas.py — Pydantic schemas for Task 1.1 output parsing.
"""
from pydantic import BaseModel, Field


class CopyVariation(BaseModel):
    """Schema for a single copy variation."""
    headline: str = Field(..., description="The main attention-grabbing headline.")
    tagline: str = Field(..., description="A short, punchy supporting tagline.")
    body: str = Field(..., description="Full body copy (2-4 sentences).")
    cta: str = Field(..., description="The Call to Action text.")


class CopyGeneratorOutput(BaseModel):
    """Schema for the full structured output with 3 copy variations."""
    variation_1: CopyVariation
    variation_2: CopyVariation
    variation_3: CopyVariation
