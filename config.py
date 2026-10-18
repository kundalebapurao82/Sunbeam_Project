"""
Sunbeam Chatbot — Centralized Configuration
All paths, API keys, model settings, and app constants.
Supports local .env as well as Streamlit Community Cloud st.secrets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env from project root if it exists ──────────────────────────────────
load_dotenv(Path(__file__).parent / ".env")


def get_secret(key: str, fallback: str = None) -> str:
    """
    Retrieve key from environment variables or Streamlit Cloud Secrets.
    """
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return fallback


# ── Project Paths ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = str(BASE_DIR / "data" / "knowledge_base")
SCRAPING_DIR = str(BASE_DIR / "scraping")

# ── API Keys ─────────────────────────────────────────────────────────────────
GROQ_API_KEY = get_secret("GROQ_API_KEY")
GEMINI_API_KEY = get_secret("Gemini_API_KEY") or get_secret("GEMINI_API_KEY")

LLM_MODEL = "openai/gpt-oss-20b"   # Groq-hosted model
LLM_TEMPERATURE = 0

EMBEDDING_MODEL = "gemini-embedding-001"   # Google Generative AI

# ── ChromaDB ─────────────────────────────────────────────────────────────────
COLLECTION_NAME = "Sunbeam_Data"

# ── App Metadata ─────────────────────────────────────────────────────────────
APP_NAME = "Sunbeam AI Assistant"
APP_ICON = "☀️"
APP_DESCRIPTION = "Your AI-powered guide to Sunbeam Infotech"

# ── Quick Action Presets ─────────────────────────────────────────────────────
QUICK_ACTIONS = [
    {
        "label": "About Sunbeam",
        "icon": "🏛️",
        "query": "Give me full information about Sunbeam Infotech Institute, its history, campuses, and vision.",
        "description": "History, vision & campuses",
    },
    {
        "label": "Explore Courses",
        "icon": "📚",
        "query": "What courses are offered at Sunbeam Infotech? Give me details on PG Diploma and other programs.",
        "description": "Browse PG Diploma & modular courses",
    },
    {
        "label": "Placements",
        "icon": "💼",
        "query": "Tell me about Sunbeam's placement statistics, hiring partners, and track record.",
        "description": "Placement rates & top recruiters",
    },
]
