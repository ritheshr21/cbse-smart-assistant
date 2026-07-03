import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.langchain_pipeline import build_chain, get_llm
from app.quiz_generator import generate_questions
from app.evaluation import evaluate_answer
from app.tracker import WeaknessTracker
from app.mcq_parser import parse_mcqs
from app.config import settings
import re

app = FastAPI()
tracker = WeaknessTracker()
qa_chain = build_chain(mode="simple")
llm = get_llm()
current_quiz = []

os.makedirs(settings.RAW_DIR, exist_ok=True)
app.mount("/pdfs", StaticFiles(directory=settings.RAW_DIR), name="pdfs")

class QueryRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: QueryRequest):
    response = qa_chain({
        "input": request.question
    })

    sources = []
    for doc in response.get("source_documents", []):
        excerpt = doc.page_content.strip()
        if len(excerpt) > 300:
            excerpt = excerpt[:300].rsplit(" ", 1)[0] + "..."

        source = {
            **doc.metadata,
            "excerpt": excerpt
        }

        chapter = doc.metadata.get("chapter")
        if chapter and os.path.exists(os.path.join(settings.RAW_DIR, f"{chapter}.pdf")):
            source["pdf_url"] = f"/pdfs/{chapter}.pdf"

        sources.append(source)

    return {
        "answer": response["answer"],
        "sources": sources
    }


@app.post("/generate-quiz")
def generate_quiz(request: QueryRequest):
    global current_quiz
    response = qa_chain({
        "input": request.question
    })

    docs = response["source_documents"]

    context = "\n\n".join([doc.page_content for doc in docs[:2]])
    quiz_text = generate_questions(llm, context)
    current_quiz = parse_mcqs(quiz_text)

    return {
        "quiz": quiz_text,
        "mcqs": current_quiz  
    }


class EvalRequest(BaseModel):
    question: str
    answer: str


class MCQAnswerRequest(BaseModel):
    answers: dict   # {"1": "A", "2": "C"}


def extract_topic(docs):
    if not docs:
        return "General"

    return docs[0].metadata.get("chapter_title") or "General"


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

    score_match = re.search(r"Total Score:\s*(\d+(?:\.\d+)?)/5", result)

    score = float(score_match.group(1)) if score_match else 0

    is_correct = score >= 3   # CBSE pass threshold

    topic = extract_topic(docs)
    tracker.update(topic, is_correct)

    return {
        "evaluation": result,
        "weak_topics": tracker.get_weak_topics(),
        "suggestions": tracker.get_suggestions()
    }



@app.post("/submit-mcq")
def submit_mcq(req: MCQAnswerRequest):
    score = 0
    total = len(current_quiz)

    results = []

    for mcq in current_quiz:
        qid = str(mcq["question_id"])
        correct = mcq["correct_answer"]

        user_ans = req.answers.get(qid, "").upper()

        is_correct = user_ans == correct

        if is_correct:
            score += 1

        results.append({
            "question_id": qid,
            "correct_answer": correct,
            "your_answer": user_ans,
            "is_correct": is_correct
        })

    return {
        "score": f"{score}/{total}",
        "details": results
    }


# Serves the built React app (frontend/dist) for production deploys where
# this backend is the single origin. In local dev, `npm run dev` serves the
# frontend instead and proxies API calls here, so dist/ won't exist yet.
_frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")