from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.retriever import get_retriever
from app.prompts import get_prompt


def get_llm():
    return OllamaLLM(model="phi")


def build_chain(mode="simple"):
    retriever = get_retriever()
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", get_prompt(mode)),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    def rag_pipeline(inputs):
        query = inputs["input"]
        chat_history = inputs.get("chat_history", [])

        # 🔎 Retrieve documents
        docs = retriever.invoke(query)

        # 🧠 Combine context
        context = "\n\n".join([doc.page_content for doc in docs])

        # 📝 Format prompt
        formatted_prompt = prompt.format(
            input=query,
            chat_history=chat_history
        )

        final_input = f"{formatted_prompt}\n\nContext:\n{context}"

        # 🤖 Call LLM
        answer = llm.invoke(final_input)

        return {
            "answer": answer,
            "context": docs
        }

    return rag_pipeline