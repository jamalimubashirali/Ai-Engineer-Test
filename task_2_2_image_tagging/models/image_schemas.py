"""
models/image_schemas.py — Pydantic schemas for Task 2.2 output parsing.
"""
from typing import List
from pydantic import BaseModel, Field


class ImageAnalysis(BaseModel):
    """Schema for a single image's AI-generated analysis."""
    filename: str = Field(..., description="Original image filename.")
    alt_text: str = Field(..., description="Descriptive alt text for accessibility.")
    tags: List[str] = Field(..., description="5–10 descriptive content tags.")
    brand_safety_score: int = Field(
        ..., ge=1, le=10,
        description="Brand safety score: 1 (unsafe) – 10 (completely safe).",
    )
    use_cases: List[str] = Field(
        ..., description="2–3 suggested advertising campaign use cases."
    )


class ImageTaggingOutput(BaseModel):
    """Wrapper for the full batch of image analyses."""
    results: List[ImageAnalysis]
