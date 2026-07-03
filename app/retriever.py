from app.vector_store import load_vector_store
from app.embeddings import get_embedding_model
from app.config import settings


def get_retriever():
    embedding_model = get_embedding_model()
    vector_store = load_vector_store(embedding_model)

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": settings.TOP_K,
            "fetch_k": settings.FETCH_K,
            "lambda_mult": settings.MMR_LAMBDA
        }
    )

    return retriever