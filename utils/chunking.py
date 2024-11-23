from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list[str]:
    """
    Split a long text into smaller chunks.

    Args:
        text (str): The cleaned text.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The overlap size between chunks.

    Returns:
        list[str]: List of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)
