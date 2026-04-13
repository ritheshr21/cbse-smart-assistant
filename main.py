from fastapi import FastAPI
from pydantic import BaseModel

from app.langchain_pipeline import build_chain

app = FastAPI()

qa_chain = build_chain(mode="simple")


class QueryRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: QueryRequest):
    response = qa_chain({
        "input": request.question,
        "chat_history": []
    })

    return {
        "answer": response["answer"]
    }