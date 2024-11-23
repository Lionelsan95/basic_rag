import re
import logging
from typing import List
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def bs4_extractor(html: str) -> str:
    """Extracts clean text from raw HTML using BeautifulSoup."""
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


def crawl_website(url: str, batch_size: int = 10, chunk_size: int = 500) -> List[dict]:
    """
    Crawls a website and processes documents into manageable chunks.

    Args:
        url (str): The URL of the website to crawl.
        batch_size (int): Number of documents to process in a batch.
        chunk_size (int): Size of each text chunk for splitting.

    Returns:
        List[dict]: List of processed text chunks.
    """
    try:
        logging.info(f"Starting to crawl: {url}")
        loader = RecursiveUrlLoader(url, extractor=bs4_extractor)

        docs, all_chunks = [], []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=0
        )

        for doc in loader.lazy_load():
            docs.append(doc)
            if len(docs) >= batch_size:
                logging.info(f"Processing a batch of {len(docs)} documents.")
                chunks = text_splitter.split_documents(docs)
                all_chunks.extend(chunks)
                docs.clear()  # Clear the batch after processing

        # Process any remaining documents
        if docs:
            logging.info(f"Processing final batch of {len(docs)} documents.")
            chunks = text_splitter.split_documents(docs)
            all_chunks.extend(chunks)

        logging.info(f"Crawling completed. Total chunks created: {len(all_chunks)}")
        return all_chunks

    except Exception as e:
        logging.error(f"An error occurred while crawling {url}: {str(e)}")
        return []
