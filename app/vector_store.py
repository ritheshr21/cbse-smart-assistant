from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def create_documents(chunks):
    return [
        Document(
            page_content=chunk["text"],
            metadata=chunk["metadata"]
        )
        for chunk in chunks
    ]


def build_vector_store(docs, embedding_model):
    return FAISS.from_documents(docs, embedding_model)


def save_vector_store(vector_store, path="faiss_index"):
    vector_store.save_local(path)