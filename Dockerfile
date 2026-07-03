# --- Stage 1: build the frontend ---
FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# --- Stage 2: backend + baked-in data/index, serving the built frontend ---
FROM python:3.11-slim
WORKDIR /app

# Runtime only serves the pre-built faiss_index/ baked in below - it doesn't
# re-run ingestion, so no need for the tesseract-ocr system package here.
# (Rebuild the index locally with `python run_pipeline.py` when data changes.)
#
# Install CPU-only torch first - sentence-transformers otherwise pulls the
# default CUDA build (adds ~7GB of unused nvidia/* packages on a CPU host).
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY main.py ./
COPY faiss_index/ ./faiss_index/
COPY data/raw/ ./data/raw/
COPY --from=frontend-build /frontend/dist ./frontend/dist

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
