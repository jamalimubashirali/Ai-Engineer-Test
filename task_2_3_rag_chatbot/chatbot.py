"""
chatbot.py — CLI entry-point for the Task 2.3 RAG Knowledge Bot.

Usage:
    python chatbot.py
    python chatbot.py --docs ./documents
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from services import build_retriever, build_rag_chain, query as rag_query


def main() -> None:
    parser = argparse.ArgumentParser(description="Agency Campaign RAG Knowledge Bot")
    parser.add_argument(
        "--docs",
        default="documents",
        help="Directory containing the agency knowledge .txt files.",
    )
    args = parser.parse_args()

    try:
        print("Loading documents and building knowledge index …")
        retriever = build_retriever(docs_dir=args.docs)
        chain = build_rag_chain(retriever)
        print("Ready!\n")
    except FileNotFoundError as err:
        print(f"Startup Error: {err}", file=sys.stderr)
        sys.exit(1)

    print("=" * 55)
    print("  Agency Campaign Knowledge Bot")
    print("  Ask about case studies or brand guidelines.")
    print("  Type 'exit' to quit.")
    print("=" * 55 + "\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if not user_input:
            continue

        print("\nThinking …")
        answer = rag_query(chain, user_input)

        print(f"\nAnswer : {answer.answer}")
        print(f"Source : {answer.source}")
        if answer.quote:
            print(f'Quote  : "{answer.quote}"')
        print()


if __name__ == "__main__":
    main()
