import re


def parse_mcqs(quiz_text):
    mcqs = []

    blocks = re.split(r"\n(?=Q\d+\s*:)", quiz_text.strip())

    for block in blocks:
        block = block.strip()

        if "Answer:" not in block:
            continue

        question_match = re.search(r"Q\d+\s*:\s*(.+)", block)
        options = re.findall(r"([A-Da-d])\)\s*(.+)", block)
        answer_match = re.search(r"Answer:\s*([A-Da-d])", block)

        if not question_match or not options or not answer_match:
            continue

        mcqs.append({
            "question_id": len(mcqs) + 1,
            "question": question_match.group(1).strip(),
            "options": [
                {"label": label.upper(), "text": text.strip()}
                for label, text in options
            ],
            "correct_answer": answer_match.group(1).upper()
        })

    return mcqs