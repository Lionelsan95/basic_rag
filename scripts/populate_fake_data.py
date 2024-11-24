from services.redis_service import mark_url_as_scraped
from services.chromadb_service import index_documents
from langchain.docstore.document import Document
import logging


def populate_redis():
    """
    Populate Redis with pre-scraped URLs for development.
    """
    urls = ["https://example.com", "https://example.org"]
    for url in urls:
        mark_url_as_scraped(url)
    logging.info("Populated Redis with pre-scraped URLs.")


def populate_chroma_db():
    """
    Populate ChromaDB with fake documents for testing purposes.
    """
    fake_documents = [
        Document(
            page_content="This is a fake document about AI.",
            metadata={"url": "https://example.com"},
        ),
        Document(
            page_content="This is another fake document about technology.",
            metadata={"url": "https://example.org"},
        ),
    ]
    index_documents(fake_documents)
    logging.info("Populated ChromaDB with fake documents.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    populate_redis()
    populate_chroma_db()
