"""
services/tagger_service.py — Vision LLM interaction layer for Task 2.2.

Uses LangChain ChatOpenAI (pointed at OpenRouter) with multimodal HumanMessage
for base64 image encoding — the correct LangChain pattern for vision API calls.
"""
import base64
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

from config import Env
from models import ImageAnalysis

# ------------------------------------------------------------------ #
#  Output parser — validates raw LLM JSON into the ImageAnalysis     #
# ------------------------------------------------------------------ #
output_parser = JsonOutputParser(pydantic_object=ImageAnalysis)

_SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp"}

_SYSTEM_PROMPT = (
    "You are an Ad Agency Creative Director and Image Analyst with expertise in "
    "brand safety and campaign strategy. Analyze the provided advertising image "
    "and return ONLY a raw JSON object with exactly these keys:\n"
    "  - 'alt_text' (string): A precise, descriptive alt text for accessibility.\n"
    "  - 'tags' (array of 5–10 strings): Descriptive content/subject tags.\n"
    "  - 'brand_safety_score' (integer 1–10): 1 = highly unsafe for brands, "
    "10 = completely safe for all advertiser categories.\n"
    "  - 'use_cases' (array of 2–3 strings): Specific campaign contexts this "
    "image would work well in (e.g. 'Instagram Story for fashion brand').\n"
    "No markdown, no backticks, no commentary — pure JSON only."
)


def _encode_image(path: str) -> tuple[str, str]:
    """
    Read an image file and return (base64_encoded_string, mime_type).

    Args:
        path: Path to the image file.

    Returns:
        Tuple of (base64 string, MIME type string).

    Raises:
        ValueError: If the file extension is not in _SUPPORTED_FORMATS.
        FileNotFoundError: If the file does not exist.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext not in _SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{ext}'. Supported formats: {_SUPPORTED_FORMATS}"
        )
    # Map extension to correct MIME type
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".png": "image/png", ".webp": "image/webp"}
    mime = mime_map.get(ext, f"image/{ext[1:]}")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8"), mime


def analyze_image(file_path: str) -> ImageAnalysis:
    """
    Send a single image to the vision LLM using LangChain's multimodal message
    format and return a validated ImageAnalysis.

    LangChain multimodal pattern:
        HumanMessage(content=[
            {"type": "text", "text": "..."},
            {"type": "image_url", "image_url": {"url": "data:<mime>;base64,<b64>"}},
        ])

    Args:
        file_path: Absolute or relative path to the image file.

    Returns:
        Validated ImageAnalysis Pydantic model.

    Raises:
        ValueError: If the file format is not supported.
        RuntimeError: On LLM or JSON parsing failure.
    """
    Env.validate()

    # Format validation happens inside _encode_image — ValueError propagates up
    b64, mime = _encode_image(file_path)
    filename = os.path.basename(file_path)

    llm = ChatOpenAI(
        base_url=Env.OPENROUTER_BASE_URL,
        api_key=Env.OPENROUTER_API_KEY,
        model=Env.VISION_MODEL,
        # Temperature 0.1 — analytical tagging; near-deterministic outputs preferred
        # for batch consistency across 5 images in the same run.
        temperature=0.1,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    # Build the multimodal message: text instruction + base64 image inline
    format_instructions = output_parser.get_format_instructions()
    messages = [
        SystemMessage(content=_SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": (
                        f"{format_instructions}\n\n"
                        "Now analyze this advertising image:"
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {
                        # Inline base64 data URI — no external URL needed
                        "url": f"data:{mime};base64,{b64}"
                    },
                },
            ]
        ),
    ]

    try:
        response = llm.invoke(messages)
        raw_json: str = response.content
        parsed: dict = output_parser.parse(raw_json)
        parsed.pop("filename", None)
        # Inject filename (added by the service layer)
        return ImageAnalysis(filename=filename, **parsed)

    except Exception as exc:
        raise RuntimeError(
            f"Failed to analyze '{filename}': {exc}"
        ) from exc
