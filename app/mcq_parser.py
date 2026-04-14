import re


def parse_mcqs(quiz_text):
    mcqs = []

    questions = re.split(r"\n\d+\.\s", quiz_text)

    for q in questions:
        if "Answer:" not in q:
            continue

        options = re.findall(r"[a-dA-D]\)\s*(.*)", q)
        answer_match = re.search(r"Answer:\s*([a-dA-D])", q)

        if not answer_match:
            continue

        correct_answer = answer_match.group(1).upper()

        mcqs.append({
            "question_id": len(mcqs) + 1,
            "options": options,
            "correct_answer": correct_answer
        })

    return mcqs