from app.data_ingestion import ingest_pdfs
from app.chunking import process_documents
from app.embeddings import get_embedding_model
from app.vector_store import create_documents, build_vector_store, save_vector_store

PDF_LINKS = [
    "https://ncert.nic.in/textbook/pdf/leph101.pdf"
]


def run():
    print("Step 1: Ingestion")
    docs = ingest_pdfs(PDF_LINKS)

    print("Step 2: Chunking")
    chunks = process_documents(docs)
    print("Chunks:", len(chunks))

    if len(chunks) == 0:
        raise ValueError("❌ No chunks created. Check PDF download or extraction.")

    print("Step 3: Embeddings")
    embedding_model = get_embedding_model()

    print("Step 4: Vector Store")
    documents = create_documents(chunks)
    vector_store = build_vector_store(documents, embedding_model)

    save_vector_store(vector_store)

    print("✅ DONE")


if __name__ == "__main__":
    run()