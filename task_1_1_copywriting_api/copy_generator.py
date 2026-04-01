"""
copy_generator.py — Entry-point for Task 1.1.

Usage:
    python copy_generator.py
    python copy_generator.py --brief "Your brief here"
"""
import argparse
import json
import sys
import os

# Ensure sibling packages resolve correctly when run as a script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from services import generate_ad_copy

DEFAULT_BRIEF = (
    "New luxury perfume for men, brand name: Noir, "
    "target: 30-45 year old professionals"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Advertising Copy Generator")
    parser.add_argument(
        "--brief",
        default=DEFAULT_BRIEF,
        help="Product / campaign brief (defaults to the Noir perfume example).",
    )
    args = parser.parse_args()

    try:
        result = generate_ad_copy(brief=args.brief)
        # Dump the validated Pydantic model as clean, indented JSON
        print(json.dumps(result.model_dump(), indent=2))
    except RuntimeError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
