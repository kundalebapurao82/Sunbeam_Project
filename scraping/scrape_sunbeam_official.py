"""
Selenium Web Scraper for Sunbeam Infotech Official Website (https://www.sunbeaminfo.com/)
Scrapes all official pages including:
- Home page
- About Us
- Courses & detailed course syllabi (PGCP-AC, PGCP-BDA, PGCP-ESD, PGCP-ITISS, PGCP-MC, etc.)
- Branches (Hinjawadi, Karad, etc.)
- Placements & Statistics
- FAQs (all categories & answers)
- Testimonials
- Contact Information
"""

import os
import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCRAPING_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRAPING_DIR, "scraped_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver

def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    clean_lines = []
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                clean_lines.append("")
                prev_blank = True
        else:
            clean_lines.append(line)
            prev_blank = False
    return "\n".join(clean_lines).strip()

def scrape_page(driver, url, wait_sec=3):
    print(f"[SCRAPING] {url}")
    try:
        driver.get(url)
        time.sleep(wait_sec)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        return driver
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return driver

def scrape_home(driver):
    scrape_page(driver, "https://www.sunbeaminfo.com/")
    body = driver.find_element(By.TAG_NAME, "body").text
    content = f"# Sunbeam Infotech — Home Page Overview\nURL: https://www.sunbeaminfo.com/\n\n{clean_text(body)}"
    out_path = os.path.join(SCRAPING_DIR, "sunbeam_home_overview.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {out_path} ({len(content)} chars)")

def scrape_about(driver):
    scrape_page(driver, "https://www.sunbeaminfo.com/about")
    body = driver.find_element(By.TAG_NAME, "body").text
    content = f"# Sunbeam Infotech — About Us\nURL: https://www.sunbeaminfo.com/about\n\n{clean_text(body)}"
    out_path = os.path.join(SCRAPING_DIR, "sunbeam_about_us.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {out_path} ({len(content)} chars)")

def scrape_branches(driver):
    scrape_page(driver, "https://www.sunbeaminfo.com/branches")
    body = driver.find_element(By.TAG_NAME, "body").text
    content = f"# Sunbeam Infotech — Branches & Campuses\nURL: https://www.sunbeaminfo.com/branches\n\n{clean_text(body)}"
    out_path = os.path.join(SCRAPING_DIR, "sunbeam_branches_campuses.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {out_path} ({len(content)} chars)")

def scrape_placements(driver):
    scrape_page(driver, "https://www.sunbeaminfo.com/placements")
    body = driver.find_element(By.TAG_NAME, "body").text
    content = f"# Sunbeam Infotech — Placements & Statistics\nURL: https://www.sunbeaminfo.com/placements\n\n{clean_text(body)}"
    out_path = os.path.join(SCRAPING_DIR, "sunbeam_placements_statistics.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {out_path} ({len(content)} chars)")

def scrape_contact(driver):
    scrape_page(driver, "https://www.sunbeaminfo.com/contact")
    body = driver.find_element(By.TAG_NAME, "body").text
    content = f"# Sunbeam Infotech — Contact Information & Admissions\nURL: https://www.sunbeaminfo.com/contact\n\n{clean_text(body)}"
    out_path = os.path.join(SCRAPING_DIR, "sunbeam_contact_info.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {out_path} ({len(content)} chars)")

def scrape_testimonials(driver):
    scrape_page(driver, "https://www.sunbeaminfo.com/testimonials")
    body = driver.find_element(By.TAG_NAME, "body").text
    content = f"# Sunbeam Infotech — Student Testimonials & Success Stories\nURL: https://www.sunbeaminfo.com/testimonials\n\n{clean_text(body)}"
    out_path = os.path.join(SCRAPING_DIR, "sunbeam_student_testimonials.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {out_path} ({len(content)} chars)")

def scrape_faqs(driver):
    scrape_page(driver, "https://www.sunbeaminfo.com/faqs", wait_sec=2)
    categories = ["General", "Admission", "Courses", "Placement", "Technical"]
    all_faq_text = ["# Sunbeam Infotech — Frequently Asked Questions (FAQs)\nURL: https://www.sunbeaminfo.com/faqs\n"]
    
    # Extract by clicking each category filter and expanding items
    for cat in categories:
        try:
            print(f"  Expanding category: {cat}")
            btns = driver.find_elements(By.XPATH, f"//button[contains(text(), '{cat}')]")
            if btns:
                driver.execute_script("arguments[0].click();", btns[0])
                time.sleep(1)
            
            # Click all collapsible questions
            acc_btns = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer')] | //button[contains(@class, 'w-full')]")
            for b in acc_btns:
                try:
                    driver.execute_script("arguments[0].click();", b)
                    time.sleep(0.05)
                except Exception:
                    pass
            time.sleep(0.5)
            
            body = driver.find_element(By.TAG_NAME, "body").text
            all_faq_text.append(f"\n## Category: {cat}\n{clean_text(body)}")
        except Exception as e:
            print(f"  FAQ category {cat} error: {e}")
            
    content = "\n\n".join(all_faq_text)
    out_path = os.path.join(SCRAPING_DIR, "sunbeam_faqs.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  -> Saved {out_path} ({len(content)} chars)")

def scrape_course_detail(driver, course_name, url):
    scrape_page(driver, url, wait_sec=3)
    
    # 1. Capture Overview text
    overview_text = driver.find_element(By.TAG_NAME, "body").text
    
    # 2. Click Syllabus Tab and click all modules to expand topics
    syllabus_text = ""
    try:
        tabs = driver.find_elements(By.XPATH, "//button[contains(text(), 'Syllabus')]")
        if tabs:
            driver.execute_script("arguments[0].click();", tabs[0])
            time.sleep(1.5)
            # Expand all '+' or accordion buttons
            plus_btns = driver.find_elements(By.XPATH, "//button[contains(text(), '+')] | //div[contains(@class, 'cursor-pointer')]")
            for pb in plus_btns:
                try:
                    driver.execute_script("arguments[0].click();", pb)
                    time.sleep(0.05)
                except Exception:
                    pass
            time.sleep(1)
            syllabus_text = driver.find_element(By.TAG_NAME, "body").text
    except Exception as e:
        print(f"  Error loading syllabus for {course_name}: {e}")
        
    combined = f"""# Course: {course_name}
URL: {url}

## Course Overview & Details:
{clean_text(overview_text)}

## Course Syllabus & Modules:
{clean_text(syllabus_text)}
"""
    safe_name = re.sub(r"\W+", "_", course_name.lower()).strip("_")
    out_path = os.path.join(SCRAPING_DIR, f"course_{safe_name}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(combined)
    print(f"  -> Saved {out_path} ({len(combined)} chars)")

def run_all_scrapers():
    print("=" * 60)
    print("  Starting Sunbeam Selenium Scraper for https://www.sunbeaminfo.com/")
    print("=" * 60)
    driver = create_driver()
    try:
        scrape_home(driver)
        scrape_about(driver)
        scrape_branches(driver)
        scrape_placements(driver)
        scrape_contact(driver)
        scrape_testimonials(driver)
        scrape_faqs(driver)

        # Scrape all 5 Post Graduate Diploma Programs
        courses = [
            ("PG Certificate Programme in Advanced Computing (PGCP-AC / DAC)", 
             "https://www.sunbeaminfo.com/courses/pg-certificate-programme-in-advanced-computing-pgcp-ac"),
            ("PG Certificate Programme in Big Data Analytics (PGCP-BDA / DBDA)", 
             "https://www.sunbeaminfo.com/courses/post-graduate-certificate-programme-in-big-data-analytics-pgcp-bda"),
            ("PG Certificate Programme in Embedded Systems Design (PGCP-ESD / DESD)", 
             "https://www.sunbeaminfo.com/courses/post-graduate-certificate-programme-in-embedded-systems-design-pgcp-esd"),
            ("PG Certificate Programme in IT Infrastructure Systems and Security (PGCP-ITISS / DITISS)", 
             "https://www.sunbeaminfo.com/courses/post-graduate-certificate-programme-in-it-infrastructure-systems-and-security-pgcp-itiss"),
            ("PG Certificate Programme in Mobile Computing (PGCP-MC / DMC)", 
             "https://www.sunbeaminfo.com/courses/post-graduate-certificate-programme-in-mobile-computing-pgcp-mc"),
        ]

        for c_name, c_url in courses:
            scrape_course_detail(driver, c_name, c_url)

    finally:
        driver.quit()
        print("\n[COMPLETE] All Sunbeam official website data scraped successfully!")

if __name__ == "__main__":
    run_all_scrapers()
