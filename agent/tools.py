"""
Sunbeam Chatbot — Agent Tools
Defines retrieval tools for semantic search against Sunbeam's knowledge base.
Includes rate limiting per query turn to prevent infinite loops while allowing
the agent to self-correct and retrieve additional context when needed.
"""

import json
from langchain_core.tools import tool
from vector_store.chroma_client import search_knowledge_base

# Global counter tracking how many times retrieval tools have been called for the current user query
_CALL_COUNT = 0
MAX_TOOL_CALLS_PER_QUERY = 3


def reset_tool_counter():
    """Reset the tool invocation counter for a new user query turn."""
    global _CALL_COUNT
    _CALL_COUNT = 0


def get_tool_call_count() -> int:
    """Return the number of times retrieval tools were invoked in the current turn."""
    global _CALL_COUNT
    return _CALL_COUNT


@tool
def get_relevant_data(query: str, top_k: int = 6) -> str:
    """
    Search and retrieve verified information from Sunbeam Institute's official knowledge base.

    Use this tool whenever you need facts regarding:
    - Sunbeam courses (PG Diploma like PGCP-AC/DAC, PGCP-BDA/DBDA, PGCP-ESD/DESD, PGCP-ITISS, PGCP-MC, modular courses)
    - Full course syllabus, duration (e.g. 1200 hours), eligibility, and modules
    - Campuses & branches (Hinjawadi IT Park Phase 2, Pune; Karad; Gultekdi)
    - Placement statistics, batch records (e.g. 94% DAC, 93% DBDA, 89% overall), and top recruiters
    - Admissions, educational loan assistance, facilities, hostel details, and FAQs
    - Contact numbers (+91 82828 29806) and official email (siit@sunbeaminfo.com)

    If the first search yields insufficient context or you need additional details to be fully confident,
    you can call this tool again with a reformulated query or higher top_k (up to 10).
    A maximum of 3 calls are allowed per user question.

    Args:
        query: Specific search query describing the information needed.
        top_k: Number of relevant passages to retrieve (default is 6; use 8 to 10 for broad inquiries).

    Returns:
        JSON string containing matched document chunks, sources, and titles.
    """
    global _CALL_COUNT
    _CALL_COUNT += 1

    if _CALL_COUNT > MAX_TOOL_CALLS_PER_QUERY:
        return json.dumps({
            "status": "limit_reached",
            "message": (
                f"Tool call limit reached ({MAX_TOOL_CALLS_PER_QUERY} calls per query). "
                "Do not make any further tool calls for this query. "
                "Synthesize a confident, comprehensive, and grounded answer using all data retrieved so far."
            ),
            "call_count": _CALL_COUNT,
            "max_allowed": MAX_TOOL_CALLS_PER_QUERY,
        }, ensure_ascii=False)

    # Clamp top_k to safe bounds
    safe_top_k = min(max(int(top_k), 3), 12)

    try:
        results = search_knowledge_base(query, top_k=safe_top_k)
        return json.dumps({
            "status": "success",
            "query": query,
            "call_number": _CALL_COUNT,
            "max_calls": MAX_TOOL_CALLS_PER_QUERY,
            "results_count": len(results),
            "results": results,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error querying knowledge base: {str(e)}",
            "call_number": _CALL_COUNT,
        }, ensure_ascii=False)


@tool
def get_sunbeam_data(user_query: str) -> str:
    """
    Legacy retrieval alias. Redirects to get_relevant_data.
    """
    return get_relevant_data.invoke({"query": user_query, "top_k": 6})
