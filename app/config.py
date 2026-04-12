import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATA_DIR = "data/"
    RAW_DIR = os.path.join(DATA_DIR, "raw/")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed/")
    
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    CHUNK_SIZE = 400
    CHUNK_OVERLAP = 50
    
    TOP_K = 4

    HF_TOKEN = os.getenv("HF_TOKEN")

settings = Settings()