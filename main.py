from fastapi import FastAPI
from pydantic import BaseModel
from app.langchain_pipeline import build_chain, get_llm
from app.quiz_generator import generate_questions
from app.evaluation import evaluate_answer
from app.tracker import WeaknessTracker

app = FastAPI()
tracker = WeaknessTracker()
qa_chain = build_chain(mode="simple")
llm = get_llm()

class QueryRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: QueryRequest):
    response = qa_chain({
        "input": request.question
    })

    return {
        "answer": response["answer"],
        "sources": [doc.metadata for doc in response.get("source_documents", [])]
    }


@app.post("/generate-quiz")
def generate_quiz(request: QueryRequest):
    response = qa_chain({
        "input": request.question
    })

    docs = response["source_documents"]

    context = "\n\n".join([doc.page_content for doc in docs[:2]])
    print("CONTEXT LENGTH:", len(context))
    print("CONTEXT SAMPLE:", context[:200])
    quiz = generate_questions(llm, context)

    return {"quiz": quiz}


class EvalRequest(BaseModel):
    question: str
    answer: str


@app.post("/evaluate")
def evaluate(req: EvalRequest):
    response = qa_chain({
        "input": req.question
    })

    docs = response["source_documents"]

    context = "\n\n".join([doc.page_content for doc in docs[:2]])

    result = evaluate_answer(
        llm,
        req.question,
        req.answer,
        context
    )

    # simple correctness check
    is_correct = "Correct: Yes" in result

    tracker.update(req.question, is_correct)

    return {
        "evaluation": result,
        "weak_topics": tracker.get_weak_topics()
    }
