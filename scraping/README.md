# 🕷️ Data Scraping Scripts

These scripts scrape data from [sunbeaminfo.in](https://www.sunbeaminfo.in/) using **Selenium WebDriver**.

> ⚠️ **These scripts require a local Chrome browser and ChromeDriver.**  
> They are NOT part of the main app — run them manually to update scraped data.

## Scripts

| Script | What it scrapes |
|--------|-----------------|
| `main.py` | Fetches all course links from the modular courses page, scrapes each course page, and stores embeddings in ChromaDB |
| `course.py` | Scrapes an individual course page (course info + accordion sections) |
| `data_scraping_about_us.py` | Scrapes the "About Us" page |
| `Internship_data.py` | Scrapes the internship page (dropdowns, tables, batch schedule) |
| `store_data_to_chromadb.py` | Master script — runs all scrapers and stores everything in ChromaDB |
| `test_chroma.py` | Quick test to list all documents in ChromaDB |

## Output Files (`.txt`)

All `.txt` files in this directory are the scraped data:
- `Sunbeam_internship_data.txt` — Internship program details
- `core_java_classes.txt`, `python_classes_in_pune.txt`, etc. — Individual course data
- `dreamllm_training_institute_pune.txt` — DreamLLM training info

## Usage

```bash
# Scrape all data and build ChromaDB
python store_data_to_chromadb.py

# Or scrape individual sections
python Internship_data.py
python main.py
```
