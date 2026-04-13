import os
import requests
import fitz
from tqdm import tqdm
from app.config import settings


def download_pdf(url: str, filename: str) -> str:
    import time

    os.makedirs(settings.RAW_DIR, exist_ok=True)
    filepath = os.path.join(settings.RAW_DIR, filename)

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


def extract_text_from_pdf(filepath: str) -> str:
    doc = fitz.open(filepath)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def ingest_pdfs(pdf_links: list):
    documents = []

    for idx, url in enumerate(tqdm(pdf_links, desc="Ingesting PDFs")):
        try:
            filename = f"chapter_{idx}.pdf"
            path = download_pdf(url, filename)
            text = extract_text_from_pdf(path)

            documents.append({
                "text": text,
                "metadata": {
                    "source_url": url,
                    "chapter": f"chapter_{idx}",
                    "subject": "physics",
                    "class": "12"
                }
            })

        except Exception as e:
            print(f"Error: {e}")

    return documents