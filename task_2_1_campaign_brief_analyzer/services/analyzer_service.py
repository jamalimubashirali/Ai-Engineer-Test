"""
services/analyzer_service.py — LLM interaction layer for Task 2.1.

Uses LangChain's ChatOpenAI (pointed at OpenRouter) for clean LCEL chain
integration: prompt | llm | parser.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from fastapi import HTTPException

from config import Env
from models import BriefAnalysis

# ------------------------------------------------------------------ #
#  Output parser — validates raw JSON into the BriefAnalysis schema  #
# ------------------------------------------------------------------ #
output_parser = JsonOutputParser(pydantic_object=BriefAnalysis)

# ------------------------------------------------------------------ #
#  Prompt template — system + human in LangChain format              #
# ------------------------------------------------------------------ #
_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an expert Chief Marketing Officer and Advertising Strategist "
                "with 20 years of experience across global campaigns. "
                "Analyze the provided campaign brief and extract structured information. "
                "Return ONLY a raw JSON object with exactly these keys:\n"
                "  - 'audience' (string): Target persona, demographics and psychographics.\n"
                "  - 'key_messages' (array of strings): The core messages to communicate.\n"
                "  - 'tone' (string): The recommended tone of voice.\n"
                "  - 'channels' (array of strings): Best distribution channels.\n"
                "  - 'risks' (array of strings): Brand safety risks or execution concerns.\n"
                "No markdown, no backticks, no commentary — pure JSON only.\n\n"
                "{format_instructions}"
            ),
        ),
        (
            "human",
            "Campaign Brief:\n\n{brief_text}",
        ),
    ]
).partial(format_instructions=output_parser.get_format_instructions())


def _build_llm() -> ChatOpenAI:
    """Construct a ChatOpenAI instance pointed at OpenRouter."""
    return ChatOpenAI(
        base_url=Env.OPENROUTER_BASE_URL,
        api_key=Env.OPENROUTER_API_KEY,
        model=Env.CHAT_MODEL,
        # Temperature 0.2 — this is analytical extraction, not creative writing.
        # Lower temperature produces consistent, reproducible structured outputs.
        temperature=0.2,
        model_kwargs={"response_format": {"type": "json_object"}},
    )


async def analyze_brief(text: str) -> BriefAnalysis:
    """
    Send a brief text through the LangChain chain and return a validated analysis.

    Chain: ChatPromptTemplate | ChatOpenAI | JsonOutputParser

    Args:
        text: Plain-text campaign brief content.

    Returns:
        A validated BriefAnalysis Pydantic model.

    Raises:
        HTTPException 500: On LLM API or parsing failure.
    """
    Env.validate()

    llm = _build_llm()
    chain = _prompt | llm | output_parser

    try:
        parsed: dict = await chain.ainvoke({"brief_text": text})
        return BriefAnalysis(**parsed)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"LLM API Error: {exc}"
        ) from exc
