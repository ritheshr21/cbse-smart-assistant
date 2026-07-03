import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATA_DIR = "data/"
    RAW_DIR = os.path.join(DATA_DIR, "raw/")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed/")
    
    # small variant (~130MB weights vs ~440MB for base) - keeps the deployed
    # container's memory footprint under free/cheap PaaS tier RAM limits
    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

    CHUNK_SIZE = 400
    CHUNK_OVERLAP = 50

    TOP_K = 4
    FETCH_K = 12
    MMR_LAMBDA = 0.5

    HF_TOKEN = os.getenv("HF_TOKEN")

    # If GROQ_API_KEY is set, the app uses Groq's hosted LLM API (needed for
    # deployment - PaaS hosts don't have the RAM/GPU to run Ollama). Locally,
    # with no key set, it falls back to Ollama for free/offline dev.
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

settings = Settings()