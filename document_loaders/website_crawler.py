import re
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter


def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


def crawl_website(url: str):
    loader = RecursiveUrlLoader(url, extractor=bs4_extractor)
    # docs = loader.load()

    docs = []
    for doc in loader.lazy_load():
        docs.append(doc)
        if len(docs) >= 10:
            # do some paged operation, e.g.
            # index.upsert(page)

            docs = []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(docs)

    return all_splits
