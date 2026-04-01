"""
q1_retry.py — Section 3 Task Q1.
Python function that calls the Anthropic API with up to 3 retries on rate-limit errors.
Uses the global Env config for the API key.
"""
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from anthropic import Anthropic, RateLimitError, APIStatusError
from config import Env

# Note: Anthropic has its own SDK; OpenRouter covers OpenAI-compatible calls.
# Task Q1 specifically asks for the Anthropic SDK, so we use it directly here.
_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", Env.OPENROUTER_API_KEY))


def generate_with_retry(
    prompt: str,
    model: str = "meta-llama/llama-3.1-8b-instruct:free",
    max_retries: int = 3,
) -> str:
    """
    Call the Anthropic API and retry up to `max_retries` times on RateLimitError.
    Implements exponential back-off between attempts.

    Args:
        prompt: User message text.
        model: Anthropic model slug.
        max_retries: Maximum retry attempts on rate-limit errors.

    Returns:
        The generated text content as a string.

    Raises:
        RateLimitError: After exhausting all retries.
        APIStatusError: For non-rate-limit API errors.
    """
    base_delay = 2  # seconds

    for attempt in range(max_retries + 1):
        try:
            response = _client.messages.create(
                model=model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text

        except RateLimitError as exc:
            if attempt < max_retries:
                wait = base_delay * (2 ** attempt)  # 2s, 4s, 8s …
                print(
                    f"[Attempt {attempt + 1}/{max_retries}] Rate limit hit — "
                    f"retrying in {wait}s …"
                )
                time.sleep(wait)
            else:
                print("Max retries exhausted.")
                raise exc

        except APIStatusError as exc:
            # Non-rate-limit HTTP error — don't retry
            print(f"API error {exc.status_code}: {exc.message}")
            raise exc


if __name__ == "__main__":
    test_prompt = "Write a 2-sentence hook for a premium coffee brand."
    try:
        result = generate_with_retry(test_prompt)
        print("Response:", result)
    except Exception as err:
        print("Failed:", err, file=sys.stderr)
        sys.exit(1)
