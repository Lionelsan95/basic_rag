import time
import hashlib


def generate_hash(value: str) -> str:
    """
    Generate a SHA256 hash for a given string.

    Args:
        value (str): The string to hash.

    Returns:
        str: The resulting hash.
    """
    return hashlib.sha256(value.encode()).hexdigest()


def measure_execution_time(func):
    """
    Decorator to measure the execution time of a function.

    Args:
        func (callable): The function to measure.

    Returns:
        callable: The wrapped function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds.")
        return result

    return wrapper


def format_retrieved_documents(retrieved_docs: list) -> str:
    """
    Format retrieved documents into a single readable context.

    Args:
        retrieved_docs (list): List of retrieved documents (each containing text and metadata).

    Returns:
        str: Formatted string combining content from all retrieved documents.
    """
    formatted_docs = []
    for idx, doc in enumerate(retrieved_docs, start=1):
        doc_content = doc.page_content.strip()
        doc_metadata = doc.metadata.get(
            "url", "Unknown Source"
        )  # Use metadata if available
        formatted_docs.append(f"[Doc {idx}] {doc_content}\n(Source: {doc_metadata})\n")

    return "\n".join(formatted_docs)
