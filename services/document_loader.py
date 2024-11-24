from langchain_community.document_loaders import RecursiveUrlLoader
from langchain.docstore.document import Document
from services.preprocessing_service import (
    clean_html_content,
    detect_language,
    preprocess_text,
    filter_quality,
)
import logging


def crawl_website(url: str, max_docs: int = 20) -> list[Document]:
    """
    Crawl a website, clean its HTML content, and preprocess the extracted text.

    Args:
        url (str): The URL of the website to crawl.
        max_docs (int): Maximum number of documents to crawl.

    Returns:
        list[Document]: List of preprocessed LangChain Document objects.
    """
    try:
        logging.info(f"Starting website crawl for: {url}")
        loader = RecursiveUrlLoader(url)
        documents = []

        for doc in loader.lazy_load():
            # Clean the raw HTML
            cleaned_content = clean_html_content(doc.page_content)

            # Detect language and filter non-English content
            if detect_language(cleaned_content) != "en":
                logging.info(f"Skipping non-English content from {url}.")
                continue

            # Preprocess the text
            preprocessed_text = preprocess_text(cleaned_content)

            # Filter out low-quality content
            if not filter_quality(preprocessed_text):
                logging.info(f"Skipping low-quality content from {url}.")
                continue

            # Add the cleaned and preprocessed content as a LangChain Document
            documents.append(
                Document(page_content=preprocessed_text, metadata=doc.metadata)
            )

            if len(documents) >= max_docs:
                logging.info(f"Reached max_docs limit of {max_docs}. Stopping crawl.")
                break

        logging.info(
            f"Successfully crawled and preprocessed {len(documents)} documents from: {url}"
        )
        return documents
    except Exception as e:
        logging.error(f"Error crawling website {url}: {e}", exc_info=True)
        raise
