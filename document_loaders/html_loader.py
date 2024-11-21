from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def loadHtmlFromUrl(url: str = "https://lilianweng.github.io/posts/2023-06-23-agent/"):
    """
    Based on a given url, load content, chunk it

    Args
        url: str
    """
    loader = WebBaseLoader(url)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    return all_splits
