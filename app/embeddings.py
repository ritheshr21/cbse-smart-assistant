import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from app.config import settings


def get_embedding_model():
    if settings.HF_TOKEN:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.HF_TOKEN

    if "bge" in settings.EMBEDDING_MODEL.lower():
        # BGE models are trained to expect an instruction prefix on the
        # query side only; embedding queries and passages identically
        # (the plain HuggingFaceEmbeddings behavior) hurts retrieval.
        return HuggingFaceBgeEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True}
        )

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )