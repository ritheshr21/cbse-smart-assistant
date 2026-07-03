from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.retriever import get_retriever
from app.prompts import get_prompt
from app.config import settings


def get_llm():
    if settings.GROQ_API_KEY:
        from langchain_groq import ChatGroq
        return ChatGroq(model=settings.GROQ_MODEL, api_key=settings.GROQ_API_KEY)

    from langchain_ollama import OllamaLLM
    return OllamaLLM(model=settings.OLLAMA_MODEL)


def build_chain(mode="simple"):
    retriever = get_retriever()
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", get_prompt(mode) + "\n\nContext:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    def rag_pipeline(inputs):
        query = inputs["input"]
        chat_history = inputs.get("chat_history", [])

        docs = retriever.invoke(query)

        context = "\n\n".join([doc.page_content for doc in docs])

        messages = prompt.format_messages(
            input=query,
            chat_history=chat_history,
            context=context
        )

        response = llm.invoke(messages)

        answer = response if isinstance(response, str) else response.content

        return {
            "answer": answer,
            "source_documents": docs
        }

    return rag_pipeline