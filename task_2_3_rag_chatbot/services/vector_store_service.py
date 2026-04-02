"""
services/vector_store_service.py — Builds and returns the Chroma retriever.
Isolated so the expensive embedding step is only run once at startup.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from config import Env


def build_retriever(docs_dir: str = "documents", k: int = 3) -> VectorStoreRetriever:
    """
    Load documents from docs_dir, split them, embed locally (HuggingFace),
    store in Chroma, and return a retriever.

    Args:
        docs_dir: Directory containing .txt knowledge files.
        k: Number of chunks to retrieve per query.

    Returns:
        A configured LangChain VectorStoreRetriever.

    Raises:
        FileNotFoundError: If no documents are found in docs_dir.
    """
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        docs_path.mkdir(parents=True)

    loader = DirectoryLoader(
        str(docs_path), glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
    )
    raw_docs = loader.load()

    if not raw_docs:
        raise FileNotFoundError(
            f"No .txt documents found in '{docs_dir}'. "
            "Add at least one knowledge file to enable retrieval."
        )

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(raw_docs)

    # Use HuggingFace locally — zero API cost. Model is read from Env so it's overridable.
    embeddings = SentenceTransformerEmbeddings(model_name=Env.EMBEDDING_MODEL)
    vectorstore = Chroma.from_documents(chunks, embeddings)

    return vectorstore.as_retriever(search_kwargs={"k": k})
