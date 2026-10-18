"""
Sunbeam Chatbot — Centralized Configuration
All paths, API keys, model settings, and app constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env from project root ──────────────────────────────────────────────
load_dotenv(Path(__file__).parent / ".env")

# ── Project Paths (relative to project root) ─────────────────────────────────
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = str(BASE_DIR / "data" / "knowledge_base")
SCRAPING_DIR = str(BASE_DIR / "scraping")

# ── API Keys ─────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("Gemini_API_KEY")

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
