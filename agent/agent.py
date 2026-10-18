"""
Sunbeam Chatbot — Agent Factory
Creates and returns the Agentic RAG agent using LangGraph's ReAct pattern.
"""

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from agent.tools import get_relevant_data, get_sunbeam_data
from agent.prompts import SYSTEM_PROMPT
from config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE


def create_sunbeam_agent():
    """
    Build and return the Sunbeam RAG agent.

    The agent uses:
        - Groq-hosted LLM for reasoning and multi-step tool calls
        - `get_relevant_data` (and legacy `get_sunbeam_data`) tools for ChromaDB semantic search
        - Confident, grounded system prompt strictly tied to retrieved data
    """
    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=LLM_TEMPERATURE,
    )

    agent = create_react_agent(
        model=llm,
        tools=[get_relevant_data, get_sunbeam_data],
        prompt=SYSTEM_PROMPT,
    )

    return agent
