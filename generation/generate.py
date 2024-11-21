from document_loaders.html_loader import loadHtmlFromUrl
from langchain_ollama import ChatOllama

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import RunnablePassthrough

from indexing.chroma_index import chroma_indexing

from document_loaders.utils import html_format_docs

all_splits = loadHtmlFromUrl()
vectorstore = chroma_indexing(all_splits)

model = ChatOllama(model="llama3.2")

RAG_TEMPLATE = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

<context>
{context}
</context>

Answer the following question:

{question}"""

rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)


def query_llm(question: str) -> str:
    retriever = vectorstore.as_retriever()

    qa_chain = (
        {"context": retriever | html_format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | model
        | StrOutputParser()
    )

    response = qa_chain.invoke(question)
    return response
