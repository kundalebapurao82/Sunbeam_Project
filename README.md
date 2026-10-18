# ☀️ Sunbeam AI Assistant

An advanced **Agentic RAG (Retrieval-Augmented Generation)** chatbot for [Sunbeam Infotech](https://www.sunbeaminfo.com/), built with LangGraph, ChromaDB, Google Generative AI Embeddings, and Streamlit.

---

## 🌟 Key Features

- **Modern Light Theme UI**: Elegant, clean, responsive design styled specifically for Sunbeam Infotech with custom card layouts, smooth micro-interactions, and instant chat access (no login required).
- **Official Knowledge Base**: Comprehensive, latest data scraped directly from the official website ([https://www.sunbeaminfo.com/](https://www.sunbeaminfo.com/)) using Selenium:
  - PG Diploma Programs: PGCP-AC (DAC), PGCP-BDA (DBDA), PGCP-ESD (DESD), PGCP-ITISS (DITISS), PGCP-MC (DMC) with full 1200-hour syllabi, modules, and eligibility.
  - Modular courses (Python, GenAI, MLOps, Java, C++, PySpark, DevOps, MERN).
  - Campuses: Pune (Hinjawadi IT Park Phase 2) and Karad.
  - Placements: Course-by-course placement statistics (DAC 94%, DBDA 93%, overall 89% across 36 batches) and recruiters.
  - Admissions, educational loan policies, third-party hostels, and contact details (+91 82828 29806 / siit@sunbeaminfo.com).
- **Agentic Multi-Step Search (`get_relevant_data`)**: The agent can perform initial retrieval and, if not fully confident, refine queries and retrieve broader context (with adaptive `top_k`).
- **Tool Call Safeguards**: Enforces a strict limit (maximum 3 calls per user question) to prevent infinite loops while empowering self-correction.
- **Confident & Grounded Answers**: Strict anti-hallucination prompts ensure the agent answers accurately and authoritatively based solely on verified Sunbeam data.
- **Lightweight Deployment**: Unnecessary archives and obsolete files removed, keeping the project clean and ready for deployment.

---

## 🏗️ Architecture

```
User Question
     ↓
┌──────────────────────┐       ┌────────────────────────┐       ┌────────────────────────┐
│  Streamlit Light UI  │──────→│  LangGraph ReAct Agent │──────→│  ChromaDB Vector Store │
│  (Modern & Clean)    │       │  (Multi-step reasoning)│       │  (286 Embedded Chunks) │
└──────────────────────┘       └────────────────────────┘       └────────────────────────┘
     ↑                                     │                                 │
     │                                     ↓                                 │
     │                              ┌───────────────┐                        │
     └──────────────────────────────│   Groq LLM    │←───────────────────────┘
                                    │ (ReAct Loop)  │   (semantic retrieval results)
                                    └───────────────┘
```

---

## 📁 Project Structure

```
├── app.py                         # Streamlit application (Light Theme, No Login)
├── config.py                      # Centralized configuration & constants
├── requirements.txt               # Python 3.11+ dependencies
├── .env                           # API keys (GROQ_API_KEY, Gemini_API_KEY)
│
├── agent/                         # Agentic RAG logic
│   ├── agent.py                   # Agent factory (LangGraph ReAct)
│   ├── tools.py                   # get_relevant_data tool with call limiting
│   └── prompts.py                 # Confident grounding system prompt
│
├── vector_store/                  # Vector database layer
│   └── chroma_client.py           # ChromaDB connection & semantic search
│
├── data/
│   └── knowledge_base/            # ChromaDB vector store (286 embedded docs)
│
├── scraping/                      # Selenium web scraping suite
│   ├── scrape_sunbeam_official.py # Official sunbeaminfo.com scraper
│   └── *.txt                      # Scraped & structured knowledge files (26 files)
│
├── scripts/
│   └── rebuild_knowledge_base.py  # Chunks & embeds all .txt files into ChromaDB
│
├── assets/                        # Architecture diagrams (pipeline.jpeg, pipeline_2.jpeg)
└── .streamlit/
    └── config.toml                # Light theme configuration
```

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure `.env`
Ensure your `.env` contains:
```env
GROQ_API_KEY=your_groq_api_key
Gemini_API_KEY=your_gemini_api_key
```

### 3. Rebuilding the Knowledge Base (Optional)
The pre-built knowledge base is already generated at `data/knowledge_base/`. To re-scrape or re-embed:
```bash
python scraping/scrape_sunbeam_official.py
python scripts/rebuild_knowledge_base.py
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Component        | Technology                                   |
|------------------|----------------------------------------------|
| Frontend         | Streamlit (Modern Custom Light Theme)        |
| Agent Framework  | LangGraph (ReAct Multi-Step Pattern)         |
| LLM Provider     | Groq                                         |
| Embeddings       | Google Generative AI (`gemini-embedding-001`)|
| Vector Database  | ChromaDB (Persistent)                        |
| Web Scraping     | Selenium WebDriver (Headless Chrome)         |
| Language         | Python 3.11+                                 |

---

## 📦 Deployment (Streamlit Cloud)

1. Push the repository to GitHub.
2. Link the repository on [Streamlit Community Cloud](https://share.streamlit.io/).
3. Set `app.py` as the main entry point.
4. In Advanced Settings, add secrets:
   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   Gemini_API_KEY = "your_gemini_api_key"
   ```
5. Deploy and access the AI Assistant immediately.
