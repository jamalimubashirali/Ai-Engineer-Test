"""
services/copy_service.py — LLM interaction layer for Task 1.1.

Uses LangChain's ChatOpenAI (pointed at OpenRouter) with a proper
prompt | llm | parser chain for clean, idiomatic LangChain integration.
"""
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from openai import RateLimitError, AuthenticationError, BadRequestError

from config import Env
from models import CopyGeneratorOutput

# ------------------------------------------------------------------ #
#  Output parser — validates and coerces raw JSON into Pydantic model #
# ------------------------------------------------------------------ #
output_parser = JsonOutputParser(pydantic_object=CopyGeneratorOutput)

# ------------------------------------------------------------------ #
#  Prompt template — system + user messages in LangChain format       #
# ------------------------------------------------------------------ #
_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an expert advertising agency copywriter. "
                "Given a product brief, generate 3 distinct variations of advertising copy. "
                "Each variation MUST include: 'headline', 'tagline', 'body', and 'cta' "
                "(Call to Action). "
                "Return ONLY a raw JSON object with keys 'variation_1', 'variation_2', "
                "'variation_3'. Each key maps to an object with the four fields above. "
                "No markdown, no backticks, no commentary — pure JSON.\n\n"
                "{format_instructions}"
            ),
        ),
        (
            "human",
            "Product Brief:\n{brief}",
        ),
    ]
).partial(format_instructions=output_parser.get_format_instructions())


def _build_llm(model: str, temperature: float) -> ChatOpenAI:
    """Construct a ChatOpenAI instance pointed at OpenRouter."""
    return ChatOpenAI(
        base_url=Env.OPENROUTER_BASE_URL,
        api_key=Env.OPENROUTER_API_KEY,
        model=model,
        # Temperature tuning:
        # 0.8 balances creative diversity across the 3 variations with
        # sufficient coherence to honour the strict JSON output constraint.
        # Lower (e.g. 0.2) → safer, more generic copy.
        # Higher (e.g. 1.2) → more unusual but risks JSON malformation.
        temperature=temperature,
        model_kwargs={"response_format": {"type": "json_object"}},
    )


def generate_ad_copy(
    brief: str,
    model: str | None = None,
    temperature: float = 0.8,
    max_retries: int = 3,
) -> CopyGeneratorOutput:
    """
    Generate 3 advertising copy variations from a product brief.

    Builds a LangChain chain:  _prompt | ChatOpenAI | JsonOutputParser
    then invokes it with retry logic for transient failures.

    Args:
        brief:        The product / campaign description.
        model:        OpenRouter model slug (defaults to Env.CHAT_MODEL).
        temperature:  Sampling temperature (see _build_llm for rationale).
        max_retries:  Retry attempts for transient errors (rate-limit, network).

    Returns:
        A validated CopyGeneratorOutput Pydantic model.

    Raises:
        RuntimeError: On auth/bad-request errors (fail fast) or exhausted retries.
    """
    Env.validate()
    resolved_model = model or Env.CHAT_MODEL

    llm = _build_llm(resolved_model, temperature)

    # LangChain LCEL chain: prompt → LLM → JSON parser
    chain = _prompt | llm | output_parser

    for attempt in range(max_retries):
        try:
            parsed: dict = chain.invoke({"brief": brief})
            return CopyGeneratorOutput(**parsed)

        except (AuthenticationError, BadRequestError) as exc:
            # Unrecoverable — wrong API key or malformed request.
            # Fail immediately; retrying would waste budget.
            raise RuntimeError(f"Unrecoverable API error: {exc}") from exc

        except RateLimitError as exc:
            # Transient — back off and retry.
            # Schedule: 1 s → 2 s → 4 s (exponential).
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(
                    f"[Attempt {attempt + 1}/{max_retries}] Rate limit hit — "
                    f"retrying in {wait}s …"
                )
                time.sleep(wait)
            else:
                raise RuntimeError(
                    f"Rate limit persisted after {max_retries} attempts."
                ) from exc

        except (OutputParserException, Exception) as exc:
            # Network errors, timeouts, JSON parse failures — potentially transient.
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(
                    f"[Attempt {attempt + 1}/{max_retries}] Error: "
                    f"{exc!r} — retrying in {wait}s …"
                )
                time.sleep(wait)
            else:
                raise RuntimeError(
                    f"Failed to generate copy after {max_retries} attempts."
                ) from exc
