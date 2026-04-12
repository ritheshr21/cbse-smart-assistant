import re
from app.config import settings


def split_into_paragraphs(text):
    return [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 50]


def semantic_chunking(text):
    paragraphs = split_into_paragraphs(text)

    chunks = []
    current = ""

    for para in paragraphs:
        if len(current.split()) + len(para.split()) <= settings.CHUNK_SIZE:
            current += " " + para
        else:
            chunks.append(current.strip())
            current = para

    if current:
        chunks.append(current.strip())

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