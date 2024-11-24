from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os
import logging
from typing import List
from langchain_core.documents import Document

# Initialize OpenAI embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")


def index_documents(
    documents: List[Document],
    persist_directory="data/db_persistent",
    batch_size=100000,
    collection_name: str = "website_docs",
):
    """
    Index documents into ChromaDB.

    Args:
        documents (list): List of LangChain Document objects.
        persist_directory (str): Directory to persist the database.
        batch_size (int): Number of documents to index in each batch.

    Returns:
        Chroma: Vectorstore with the indexed documents.
    """
    try:
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize or load Chroma vectorstore
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_function=embeddings,
        )
        # Index documents in batches for efficiency
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            vectorstore.add_documents(batch)
            logging.info(
                f"Indexed batch {i // batch_size + 1}: {len(batch)} documents."
            )

        logging.info(f"Indexed a total of {len(documents)} documents into ChromaDB.")
        return vectorstore
    except Exception as e:
        logging.error(f"Error indexing documents: {e}", exc_info=True)
        raise


def get_relevant_documents(
    query,
    n_results=3,
    persist_directory="data/db_persistent",
    collection_name: str = "website_docs",
):
    """
    Retrieve relevant context for a query from ChromaDB.

    Args:
        query (str): The user's query.
        n_results (int): Number of top results to retrieve.
        persist_directory (str): Directory where the database is persisted.

    Returns:
        list: List of relevant LangChain Document objects.
    """
    try:
        # Load the Chroma vectorstore
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_function=embeddings,
        )

        # Perform similarity search
        results = vectorstore.similarity_search(query=query)
        logging.info(f"Retrieved {len(results)} documents for the query: '{query}'")
        return results
    except Exception as e:
        logging.error(f"Error retrieving documents: {e}", exc_info=True)
        raise
