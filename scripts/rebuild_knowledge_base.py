"""
Rebuild Knowledge Base
Reads all scraped .txt files, chunks them, embeds with Google Generative AI,
and stores in ChromaDB at data/knowledge_base/.

Run this once before deployment or whenever scraped data changes.
Usage:  python scripts/rebuild_knowledge_base.py
"""

import os
import sys
import re
import shutil
import time

# Add project root to path so we can import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from dotenv import load_dotenv

from config import KNOWLEDGE_BASE_PATH, GEMINI_API_KEY, EMBEDDING_MODEL, COLLECTION_NAME, SCRAPING_DIR


def rebuild_knowledge_base():
    """
    Rebuild the entire ChromaDB knowledge base from scraped .txt files.
    """
    load_dotenv()

    print("=" * 60)
    print("  Sunbeam Knowledge Base Rebuilder")
    print("=" * 60)

    # ── Step 1: Initialize embedding model ────────────────────────────────
    print("\n[1/4] Initializing Google Generative AI embedding model...")
    embed_model = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
    )
    print(f"       Model: {EMBEDDING_MODEL}")

    # ── Step 2: Reset knowledge base ──────────────────────────────────────
    print("\n[2/4] Resetting knowledge base...")
    if os.path.exists(KNOWLEDGE_BASE_PATH):
        shutil.rmtree(KNOWLEDGE_BASE_PATH)
        print(f"       Deleted old: {KNOWLEDGE_BASE_PATH}")
    os.makedirs(KNOWLEDGE_BASE_PATH, exist_ok=True)

    db = chromadb.PersistentClient(path=KNOWLEDGE_BASE_PATH)
    collection = db.get_or_create_collection(COLLECTION_NAME)
    print(f"       Collection: {COLLECTION_NAME}")

    # ── Step 3: Chunk & embed all .txt files ──────────────────────────────
    print("\n[3/4] Processing scraped data files...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
    )

    txt_files = sorted(
        f for f in os.listdir(SCRAPING_DIR) if f.endswith(".txt")
    )

    if not txt_files:
        print("       [ERROR] No .txt files found in scraping directory!")
        print(f"       Looked in: {SCRAPING_DIR}")
        return

    total_chunks = 0
    for txt_file in txt_files:
        filepath = os.path.join(SCRAPING_DIR, txt_file)
        print(f"\n       [FILE] {txt_file}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            print("          [WARN] Empty file, skipped")
            continue

        chunks = splitter.split_text(content)

        safe_name = re.sub(r"\W+", "_", txt_file.replace(".txt", ""))
        batch_size = 20
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i : i + batch_size]
            batch_ids = [f"{safe_name}_{i + j}" for j in range(len(batch_chunks))]
            batch_embeddings = None
            for attempt in range(6):
                try:
                    batch_embeddings = embed_model.embed_documents(batch_chunks)
                    break
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        wait_sec = (attempt + 1) * 3
                        print(f"          [RATE LIMIT] Exceeded quota, waiting {wait_sec}s before retry (attempt {attempt + 1}/6)...")
                        time.sleep(wait_sec)
                    else:
                        raise e
            if batch_embeddings is None:
                raise RuntimeError(f"Failed to embed batch for {txt_file} after retries")
            time.sleep(1.0)
            batch_metadatas = []
            for j, chunk in enumerate(batch_chunks):
                first_line = "Unknown"
                for line in chunk.strip().splitlines():
                    line = line.strip()
                    if line:
                        first_line = line[:100]
                        break
                batch_metadatas.append({
                    "source": txt_file,
                    "title": first_line,
                    "chunk_index": i + j,
                })
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                documents=batch_chunks,
                metadatas=batch_metadatas,
            )

        print(f"          -> {len(chunks)} chunks embedded")
        total_chunks += len(chunks)

    # ── Step 4: Summary ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  [OK] Knowledge base rebuilt successfully!")
    print(f"  Files processed: {len(txt_files)}")
    print(f"  Total chunks:    {total_chunks}")
    print(f"  Total docs in DB: {collection.count()}")
    print(f"  Location: {KNOWLEDGE_BASE_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    rebuild_knowledge_base()
