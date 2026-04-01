"""
services/rag_service.py — RAG chain construction and query logic for Task 2.3.
"""
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import RetrievalQA
from langchain_core.vectorstores import VectorStoreRetriever

from config import Env
from models import ChatAnswer

output_parser = JsonOutputParser(pydantic_object=ChatAnswer)

_TEMPLATE = """
You are a strict agency knowledge assistant. Answer questions ONLY from the provided context.
If the answer is not in the context, respond with this exact JSON:
{{"answer": "I cannot find this information in the provided documents.", "source": "N/A", "quote": ""}}

You MUST respond in valid JSON with exactly these keys: "answer", "source", "quote".
- "answer": Your factual answer.
- "source": The source document name (from the metadata).
- "quote": A direct verbatim quote from the context that supports your answer.

{format_instructions}

Context:
{context}

Question: {question}

JSON Response:"""


def build_rag_chain(retriever: VectorStoreRetriever) -> RetrievalQA:
    """
    Build a LangChain RetrievalQA chain with strict JSON output parsing.

    Args:
        retriever: Pre-built vector store retriever from vector_store_service.

    Returns:
        A configured RetrievalQA chain.
    """
    Env.validate()

    llm = ChatOpenAI(
        base_url=Env.OPENROUTER_BASE_URL,
        api_key=Env.OPENROUTER_API_KEY,
        model=Env.CHAT_MODEL,
        temperature=0.0,  # Deterministic — no creativity for factual retrieval
    )

    prompt = PromptTemplate(
        template=_TEMPLATE,
        input_variables=["context", "question"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return chain


def query(chain: RetrievalQA, question: str) -> ChatAnswer:
    """
    Run a question through the RAG chain and return a validated ChatAnswer.

    Args:
        chain: The pre-built RetrievalQA chain.
        question: User's natural-language question.

    Returns:
        A validated ChatAnswer Pydantic model.
    """
    result = chain.invoke({"query": question})
    raw_output: str = result["result"]

    try:
        parsed: dict = output_parser.parse(raw_output)
        return ChatAnswer(**parsed)
    except Exception:
        # Graceful fallback if the LLM didn't perfectly follow schema
        return ChatAnswer(
            answer=raw_output,
            source="Unknown",
            quote="",
        )
