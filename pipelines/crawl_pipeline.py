import logging
from services.document_loader import crawl_website
from services.chromadb_service import index_documents
from services.redis_service import is_url_scraped, mark_url_as_scraped
from celery_app import celery_app

def crawl_and_index_pipeline(url: str) -> str:
    """
    Crawl a website and index its content into ChromaDB.

    Args:
        url (str): The URL to scrape and index.

    Returns:
        str: Success message or raises an error.
    """
    try:
        # Step 1: Check if the URL has already been processed
        if is_url_scraped(url):
            logging.info(f"URL '{url}' has already been scraped. Skipping crawling.")
            return f"URL '{url}' is already processed and indexed."

        # Step 2: Crawl the website
        logging.info(f"Crawling website: {url}")
        documents = crawl_website(url)
        if not documents:
            raise ValueError(f"No documents found for URL: {url}")

        # Step 3: Index the documents into ChromaDB
        logging.info(f"Indexing {len(documents)} documents.")
        index_documents(documents)

        # Mark the URL as processed
        mark_url_as_scraped(url)

        logging.info(f"URL '{url}' successfully processed and indexed.")
        return f"URL '{url}' successfully processed and indexed."
    except Exception as e:
        logging.error(f"Error in crawling and indexing pipeline: {e}", exc_info=True)
        raise

@celery_app.task
def async_crawl_and_index_pipeline(url: str) -> str:
    """
    Celery task to crawl a website and index its content into ChromaDB.

    Args:
        url (str): The URL to scrape and index.

    Returns:
        str: Success message or raises an error.
    """
    try:
        logging.info(f"Crawling website: {url}")
        documents = crawl_website(url)
        if not documents:
            raise ValueError(f"No documents found for URL: {url}")

        logging.info(f"Indexing {len(documents)} documents.")
        index_documents(documents)

        mark_url_as_scraped(url)

        logging.info(f"URL '{url}' successfully processed and indexed.")
        return f"URL '{url}' successfully processed and indexed."
    except Exception as e:
        logging.error(f"Error in async crawling and indexing pipeline: {e}", exc_info=True)
        raise
