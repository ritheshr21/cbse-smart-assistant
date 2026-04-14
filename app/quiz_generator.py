from langchain_core.prompts import PromptTemplate


def generate_questions(llm, context, num_questions=3):
    prompt = PromptTemplate(
        input_variables=["context", "num"],
        template = """
You are a CBSE examiner.

You MUST generate MCQ questions in EXACT format.

DO NOT generate descriptive questions.
DO NOT generate paragraphs.
ONLY generate MCQs.

Generate EXACTLY:

Q1: <question>
Options:
A) <option>
B) <option>
C) <option>
D) <option>
Answer: <A/B/C/D>

Q2: <question>
Options:
A) <option>
B) <option>
C) <option>
D) <option>
Answer: <A/B/C/D>

Q3: <question>
Options:
A) <option>
B) <option>
C) <option>
D) <option>
Answer: <A/B/C/D>

Context:
{context}
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "num": num_questions
    })
    output = response.content if hasattr(response, "content") else response
    if not output or len(output.strip()) < 20 or output.strip() == "..":
        return "Unable to generate quiz properly. Try another question or improve context."
    
    return output.strip()

