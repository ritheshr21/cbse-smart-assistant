from fastapi import FastAPI
from pydantic import BaseModel
from app.langchain_pipeline import build_chain, get_llm
from app.quiz_generator import generate_questions
from app.evaluation import evaluate_answer
from app.tracker import WeaknessTracker
from app.mcq_parser import parse_mcqs

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
    global current_quiz
    response = qa_chain({
        "input": request.question
    })

    docs = response["source_documents"]

    context = "\n\n".join([doc.page_content for doc in docs[:2]])
    quiz_text = generate_questions(llm, context)
    current_quiz = parse_mcqs(quiz_text)

    print("QUIZ RAW OUTPUT:\n", quiz_text)
    return {
        "quiz": quiz_text,
        "mcqs": current_quiz  
    }


class EvalRequest(BaseModel):
    question: str
    answer: str


class MCQAnswerRequest(BaseModel):
    answers: dict   # {"1": "A", "2": "C"}


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