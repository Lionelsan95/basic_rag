from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


local_embeddings = OllamaEmbeddings(model="nomic-embed-text")


def chroma_indexing(docs):
    vectorstore = Chroma.from_documents(documents=docs, embedding=local_embeddings)
    return vectorstore
