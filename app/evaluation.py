from langchain_core.prompts import PromptTemplate


def evaluate_answer(llm, question, user_answer, context):
    prompt = PromptTemplate(
        input_variables=["question", "user_answer", "context"],
        template="""
You are a CBSE board examiner.

Evaluate the student's answer strictly based on CBSE marking scheme.

Question:
{question}

Student Answer:
{user_answer}

Reference Context:
{context}

Evaluate using this marking scheme:

1. Content Accuracy (0–2 marks)
2. Explanation / Key Points (0–2 marks)
3. Clarity & Presentation (0–1 mark)

Rules:
- Be strict but fair
- Do not give full marks unless perfect
- Mention missing points clearly

Output EXACTLY in this format:

Content Accuracy: <marks>/2
Explanation: <marks>/2
Clarity: <marks>/1

Total Score: <X>/5

Evaluation:
<2-3 lines feedback>

Weak Areas:
- <point 1>
- <point 2>
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "user_answer": user_answer,
        "context": context
    })

    return response.content if hasattr(response, "content") else response