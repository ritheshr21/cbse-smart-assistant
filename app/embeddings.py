import os
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings


def get_embedding_model():
    # 🔐 Set token globally
    if settings.HF_TOKEN:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.HF_TOKEN

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )