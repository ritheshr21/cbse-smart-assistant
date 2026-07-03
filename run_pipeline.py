from app.data_ingestion import ingest_pdfs
from app.chunking import process_documents
from app.embeddings import get_embedding_model
from app.vector_store import create_documents, build_vector_store, save_vector_store

# ncert.nic.in is currently unreachable, so per-chapter downloads (Maths)
# are disabled for now. Class 10 Science is supplied locally as a single
# combined PDF (all chapters) instead. "url" is just a filename here -
# download_pdf() finds it already in data/raw/ and skips fetching.
PDF_LINKS = [
    {
        "url": "NCERT-Class-10-Science.pdf",
        "subject": "science",
        "class": "10",
    },
]


def run():
    print("Step 1: Ingestion")
    docs = ingest_pdfs(PDF_LINKS)

    print("Step 2: Chunking")
    chunks = process_documents(docs)
    print("Chunks:", len(chunks))

    if len(chunks) == 0:
        raise ValueError("No chunks created. Check PDF download or extraction.")

    print("Step 3: Embeddings")
    embedding_model = get_embedding_model()

    print("Step 4: Vector Store")
    documents = create_documents(chunks)
    vector_store = build_vector_store(documents, embedding_model)

    save_vector_store(vector_store)

    print("DONE")


if __name__ == "__main__":
    run()