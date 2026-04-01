"""
routers/brief_router.py — FastAPI router for Task 2.1 endpoints.

Endpoints:
  POST /analyze-brief          — JSON body with brief_text → structured BriefAnalysis
  POST /analyze-brief/upload   — PDF file upload → structured BriefAnalysis
  POST /analyze-brief/stream   — JSON body + SSE streaming response (Bonus)
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import fitz  # PyMuPDF
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from models import BriefAnalysis
from services import analyze_brief
from config import Env

router = APIRouter(prefix="/analyze-brief", tags=["Campaign Brief Analyzer"])


class AnalyzeRequest(BaseModel):
    brief_text: str


# ------------------------------------------------------------------ #
#  POST /analyze-brief — plain-text JSON body                        #
# ------------------------------------------------------------------ #
@router.post("", response_model=BriefAnalysis, summary="Analyze plain-text brief")
async def analyze_text_brief(request: AnalyzeRequest) -> BriefAnalysis:
    """Accept a JSON body with `brief_text` and return a structured analysis."""
    if not request.brief_text.strip():
        raise HTTPException(status_code=400, detail="brief_text cannot be empty.")
    return await analyze_brief(request.brief_text)


# ------------------------------------------------------------------ #
#  POST /analyze-brief/upload — PDF file upload (Bonus)              #
# ------------------------------------------------------------------ #
@router.post(
    "/upload",
    response_model=BriefAnalysis,
    summary="Upload a PDF brief and receive structured analysis",
)
async def analyze_pdf_brief(file: UploadFile = File(...)) -> BriefAnalysis:
    """Accept a PDF upload, extract text with PyMuPDF, and return structured analysis."""
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        text = "".join(page.get_text() for page in doc)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"PDF parsing failed: {exc}"
        ) from exc

    if not text.strip():
        raise HTTPException(
            status_code=400, detail="No extractable text found in PDF."
        )

    return await analyze_brief(text)


# ------------------------------------------------------------------ #
#  POST /analyze-brief/stream — SSE streaming response (Bonus +5 pts)#
# ------------------------------------------------------------------ #
def _build_sse_chain():
    """Return the LangChain chain used for SSE token streaming."""
    output_parser = JsonOutputParser(pydantic_object=BriefAnalysis)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an expert Chief Marketing Officer. "
                    "Analyze the campaign brief and return ONLY a JSON object with "
                    "keys: audience, key_messages (array), tone, channels (array), "
                    "risks (array). No markdown, no backticks — pure JSON.\n\n"
                    "{format_instructions}"
                ),
            ),
            ("human", "Campaign Brief:\n\n{brief_text}"),
        ]
    ).partial(format_instructions=output_parser.get_format_instructions())

    llm = ChatOpenAI(
        base_url=Env.OPENROUTER_BASE_URL,
        api_key=Env.OPENROUTER_API_KEY,
        model=Env.CHAT_MODEL,
        temperature=0.2,
        streaming=True,  # Enable token-by-token streaming
    )
    return prompt | llm


async def _sse_generator(brief_text: str):
    """Async generator that yields SSE-formatted tokens from the LLM stream."""
    chain = _build_sse_chain()
    try:
        async for chunk in chain.astream({"brief_text": brief_text}):
            token = chunk.content if hasattr(chunk, "content") else str(chunk)
            if token:
                # SSE format: each message is "data: <payload>\n\n"
                yield f"data: {json.dumps({'token': token})}\n\n"
        # Signal stream completion
        yield "data: [DONE]\n\n"
    except Exception as exc:
        yield f"data: {json.dumps({'error': str(exc)})}\n\n"


@router.post(
    "/stream",
    summary="Stream analysis tokens via Server-Sent Events (SSE)",
    description=(
        "Accepts a JSON body with `brief_text` and returns a streaming SSE response. "
        "Each event contains a `token` field. The final event is `[DONE]`. "
        "Assemble all tokens to reconstruct the full JSON analysis."
    ),
)
async def stream_brief_analysis(request: AnalyzeRequest) -> StreamingResponse:
    """Stream the LLM analysis token-by-token using Server-Sent Events."""
    if not request.brief_text.strip():
        raise HTTPException(status_code=400, detail="brief_text cannot be empty.")

    Env.validate()

    return StreamingResponse(
        _sse_generator(request.brief_text),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering for true streaming
        },
    )
