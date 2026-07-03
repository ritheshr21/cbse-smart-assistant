import os
import re
from collections import Counter
import requests
import fitz
import pytesseract
from PIL import Image
from tqdm import tqdm
from app.config import settings

pytesseract.pytesseract.tesseract_cmd = os.getenv(
    "TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def download_pdf(url: str, filename: str) -> str:
    import time

    os.makedirs(settings.RAW_DIR, exist_ok=True)
    filepath = os.path.join(settings.RAW_DIR, filename)

    if os.path.exists(filepath):
        return filepath

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            return filepath

        except Exception as e:
            print(f"Retry {attempt+1} failed: {e}")
            time.sleep(2)

    raise Exception("Failed to download PDF after retries")


PAGE_NUMBER_RE = re.compile(r'^\d+$')
REPRINT_RE = re.compile(r'^reprint\s+\d{4}-\d{2,4}$', re.IGNORECASE)


def _clean_pages(pages_text):
    """Drop running headers/footers (chapter/subject titles, page numbers,
    reprint stamps) that NCERT repeats on nearly every page and would
    otherwise get embedded as if they were content."""
    line_counts = Counter()

    for text in pages_text:
        for line in {l.strip() for l in text.split("\n") if l.strip()}:
            line_counts[line] += 1

    n_pages = len(pages_text)
    boilerplate_threshold = max(2, int(n_pages * 0.3))
    boilerplate = {
        line for line, count in line_counts.items()
        if count >= boilerplate_threshold and len(line) < 60
    }

    cleaned_pages = []
    for text in pages_text:
        kept_lines = []
        for line in text.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped in boilerplate:
                continue
            if PAGE_NUMBER_RE.match(stripped):
                continue
            if REPRINT_RE.match(stripped):
                continue
            kept_lines.append(stripped)
        cleaned_pages.append("\n".join(kept_lines))

    return cleaned_pages


def _extract_chapter_title(first_page_text, fallback):
    lines = [l.strip() for l in first_page_text.split("\n") if l.strip()]

    started = False
    title_lines = []

    for line in lines:
        if re.match(r'^chapter\b', line, re.IGNORECASE):
            started = True
            continue

        if not started:
            continue

        if re.match(r'^\d+(\.\d+)*\s', line) or len(title_lines) >= 4:
            break

        title_lines.append(line)

    if title_lines:
        return " ".join(title_lines).title()

    return fallback


def _is_garbled(text, sample_size=500):
    """Some PDFs scramble their font encoding (glyphs render correctly but
    character codes don't map to real Unicode letters) to block copy/paste.
    Detect that by checking how much of the text looks like real letters."""
    sample = text[:sample_size]
    non_space = sum(1 for c in sample if not c.isspace())
    if non_space < 20:
        return False
    letters = sum(1 for c in sample if c.isalpha() and c.isascii())
    return (letters / non_space) < 0.5


def _ocr_page(page, dpi=300):
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img)


def extract_text_from_pdf(filepath: str, fallback_title: str = "Untitled Chapter"):
    doc = fitz.open(filepath)

    pages_text = []
    for page in doc:
        text = page.get_text()
        if _is_garbled(text):
            text = _ocr_page(page)
        pages_text.append(text)

    chapter_title = _extract_chapter_title(pages_text[0], fallback_title) if pages_text else fallback_title

    text = "\n\n".join(_clean_pages(pages_text))

    return text, chapter_title


def ingest_pdfs(pdf_specs: list):
    """pdf_specs: list of {"url": str, "subject": str, "class": str}"""
    documents = []

    for spec in tqdm(pdf_specs, desc="Ingesting PDFs"):
        url = spec["url"]

        try:
            filename = os.path.basename(url)
            chapter_id = os.path.splitext(filename)[0]

            path = download_pdf(url, filename)
            text, chapter_title = extract_text_from_pdf(path, fallback_title=chapter_id)

            documents.append({
                "text": text,
                "metadata": {
                    "source_url": url,
                    "chapter": chapter_id,
                    "chapter_title": chapter_title,
                    "subject": spec.get("subject", "unknown"),
                    "class": spec.get("class", "unknown")
                }
            })

        except Exception as e:
            print(f"Error ingesting {url}: {e}")

    return documents