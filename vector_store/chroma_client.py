"""
Sunbeam Chatbot — ChromaDB Client
Handles connection to the persistent vector database and semantic search.
Uses Google Generative AI embeddings (works locally + on Streamlit Cloud).
"""

import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import KNOWLEDGE_BASE_PATH, GEMINI_API_KEY, EMBEDDING_MODEL, COLLECTION_NAME


def _get_embedding_model():
    """Initialize the Google Generative AI embedding model."""
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
    )


def _get_collection():
    """Connect to the persistent ChromaDB and return the collection."""
    db = chromadb.PersistentClient(path=KNOWLEDGE_BASE_PATH)
    return db.get_or_create_collection(COLLECTION_NAME)


# Module-level singletons (created once, reused across requests)
embed_model = _get_embedding_model()
collection = _get_collection()


def search_knowledge_base(query: str, top_k: int = 6) -> list[dict]:
    """
    Perform semantic search against the Sunbeam knowledge base.

    Args:
        query: The natural-language search query.
        top_k: Number of top results to return (default is 6).

    Returns:
        A list of dicts, each with 'document' and 'metadata' keys.
    """
    query_embedding = embed_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    matched = []
    if results and "documents" in results and results["documents"] and results["documents"][0]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            matched.append({"document": doc, "metadata": meta})

    return matched
