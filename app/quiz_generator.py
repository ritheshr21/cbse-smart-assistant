from langchain_core.prompts import PromptTemplate


def generate_questions(llm, context, num_questions=3):
    prompt = PromptTemplate(
        input_variables=["context", "num"],
        template = """
You are a CBSE examiner.

Your task is to generate questions strictly from the given context.

Rules:
- Do NOT ask for clarification
- Do NOT say anything else
- Do NOT return empty or dots
- Always generate full questions

Generate EXACTLY this format:

Q1: <MCQ question>
Options:
A) ...
B) ...
C) ...
D) ...
Answer: <correct option>

Q2: <MCQ question>
Options:
A) ...
B) ...
C) ...
D) ...
Answer: <correct option>

Q3: <Subjective question>

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

