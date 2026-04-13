from langchain_core.prompts import PromptTemplate


def evaluate_answer(llm, question, user_answer, correct_context):
    prompt = PromptTemplate(
        input_variables=["question", "user_answer", "context"],
        template="""
You are a strict CBSE evaluator.

Question:
{question}

Student Answer:
{user_answer}

Reference Context:
{context}

Evaluate:
- Is the answer correct? (Yes/No)
- Give a score out of 5
- Suggest improvement

Output format:
Correct:
Score:
Feedback:
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "user_answer": user_answer,
        "context": correct_context
    })

    return response.content if hasattr(response, "content") else response