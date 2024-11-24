from services.chromadb_service import index_documents
import os
import logging


def clear_chroma_db(persist_directory="data/db_persistent"):
    """
    Clears the ChromaDB storage directory.

    Args:
        persist_directory (str): Path to the ChromaDB storage directory.
    """
    if os.path.exists(persist_directory):
        for file in os.listdir(persist_directory):
            file_path = os.path.join(persist_directory, file)
            os.remove(file_path)
        logging.info(f"Cleared ChromaDB directory: {persist_directory}")
    else:
        logging.warning(f"ChromaDB directory does not exist: {persist_directory}")


def initialize_chroma_db():
    """
    Initializes ChromaDB with default content for development or testing.
    """
    try:
        logging.info("Initializing ChromaDB with sample documents...")
        sample_docs = [
            {"content": "Sample document 1", "metadata": {"source": "test_source"}},
            {"content": "Sample document 2", "metadata": {"source": "test_source"}},
        ]
        index_documents(sample_docs)
        logging.info("ChromaDB initialization complete.")
    except Exception as e:
        logging.error(f"Error initializing ChromaDB: {e}", exc_info=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    clear_chroma_db()
    initialize_chroma_db()
