import re
from app.config import settings


def split_into_paragraphs(text):
    return [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 50]


def semantic_chunking(text):
    paragraphs = split_into_paragraphs(text)

    chunk_size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP

    chunks = []
    current_words = []

    def flush():
        if current_words:
            chunks.append(" ".join(current_words))

    for para in paragraphs:
        para_words = para.split()

        if len(para_words) > chunk_size:
            flush()
            start = 0
            while start < len(para_words):
                end = start + chunk_size
                chunks.append(" ".join(para_words[start:end]))
                start = end - overlap if end - overlap > start else end
            current_words = []
            continue

        if len(current_words) + len(para_words) <= chunk_size:
            current_words.extend(para_words)
        else:
            flush()
            current_words = (current_words[-overlap:] if overlap else []) + para_words

    flush()

    return chunks


def process_documents(documents):
    results = []

    for doc in documents:
        chunks = semantic_chunking(doc["text"])

        for chunk in chunks:
            results.append({
                "text": chunk,
                "metadata": doc["metadata"]
            })

    return results