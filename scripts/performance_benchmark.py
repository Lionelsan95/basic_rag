import time
from services.chromadb_service import index_documents, retrieve_context
from services.document_loader import crawl_website


def benchmark_crawling(url: str):
    """
    Benchmark the time taken to crawl a website.
    """
    start_time = time.time()
    documents = crawl_website(url)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Crawled {len(documents)} documents in {elapsed_time:.2f} seconds.")


def benchmark_indexing(documents):
    """
    Benchmark the time taken to index documents into ChromaDB.
    """
    start_time = time.time()
    index_documents(documents)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Indexed {len(documents)} documents in {elapsed_time:.2f} seconds.")


def benchmark_querying(query: str):
    """
    Benchmark the time taken to retrieve context from ChromaDB.
    """
    start_time = time.time()
    results = retrieve_context(query)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Retrieved {len(results)} results in {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    url = "https://example.com"
    query = "What is AI?"

    print("=== Benchmarking ===")
    benchmark_crawling(url)

    # Example documents for benchmarking indexing
    fake_documents = [
        {"content": "Fake document 1", "metadata": {"source": "test_source"}},
        {"content": "Fake document 2", "metadata": {"source": "test_source"}},
    ]
    benchmark_indexing(fake_documents)
    benchmark_querying(query)
