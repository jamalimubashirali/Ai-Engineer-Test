"""
config/env.py — Central environment configuration for the entire project.

All modules should import from here instead of calling os.environ directly.
Load a .env file at the project root before importing this module
(e.g., `from dotenv import load_dotenv; load_dotenv()`).
"""
import os
from dotenv import load_dotenv

# Load .env from the project root (one directory above config/)
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_root, ".env"))


class Env:
    """Centralised, typed access to all environment variables."""

    # ------------------------------------------------------------------ #
    #  LLM Gateway                                                         #
    # ------------------------------------------------------------------ #
    OPENROUTER_API_KEY: str = os.environ.get("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    # ------------------------------------------------------------------ #
    #  Model selection (override via .env to switch models globally)       #
    # ------------------------------------------------------------------ #
    # Free-tier models on OpenRouter — no credits required.
    # Override either value in .env to switch models globally.
    CHAT_MODEL: str = os.environ.get("CHAT_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    VISION_MODEL: str = os.environ.get("VISION_MODEL", "nvidia/nemotron-nano-12b-v2-vl:free")

    # Embedding model used by Task 2.3 (runs locally via HuggingFace, no API key needed).
    EMBEDDING_MODEL: str = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # ------------------------------------------------------------------ #
    #  Validation helper                                                   #
    # ------------------------------------------------------------------ #
    @classmethod
    def validate(cls) -> None:
        """Raise an error early if critical variables are missing."""
        if not cls.OPENROUTER_API_KEY:
            raise EnvironmentError(
                "OPENROUTER_API_KEY is not set. "
                "Copy .env.example to .env and fill in your key."
            )
