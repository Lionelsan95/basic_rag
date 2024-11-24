import logging
from pipelines.crawl_pipeline import (
    crawl_and_index_pipeline,
    async_crawl_and_index_pipeline,
)
from pipelines.query_pipeline import run_query_pipeline
from utils.logging_config import configure_logging
from utils.validators import is_valid_url


def main():
    """
    CLI entry point for the application.
    This script allows users to interact with the RAG pipeline.
    """
    # Configure logging
    configure_logging(log_file="app.log")

    print("==> Local Basic RAG CLI <==")

    try:
        while True:
            # Step 1: Choose operation mode
            print("\nSelect an operation:")
            print("1. Crawl and index a website (sync)")
            print("2. Crawl and index a website (async)")
            print("3. Query the system")
            print("4. Exit")
            choice = input("Enter your choice (1/2/3/4): ").strip()

            if choice == "4":
                print("Goodbye!")
                logging.info("User exited the CLI.")
                break

            if choice not in {"1", "2", "3"}:
                print("Invalid choice. Please select a valid option.")
                continue

            # Handle operations based on user choice
            if choice == "1":
                # Synchronous crawling and indexing
                url = input("Enter the website URL: ").strip()
                if not is_valid_url(url):
                    print("Invalid URL. Please try again.")
                    logging.warning(f"Invalid URL entered: {url}")
                    continue
                try:
                    print(f"Synchronously crawling and indexing {url}...")
                    response = crawl_and_index_pipeline(url)
                    print(f"\n{response}\n")
                except Exception as e:
                    print("An error occurred while processing the URL.")
                    logging.error(f"Error in synchronous crawling: {e}", exc_info=True)

            elif choice == "2":
                # Asynchronous crawling and indexing
                url = input("Enter the website URL: ").strip()
                if not is_valid_url(url):
                    print("Invalid URL. Please try again.")
                    logging.warning(f"Invalid URL entered: {url}")
                    continue
                try:
                    print(f"Asynchronously crawling and indexing {url}...")
                    task_id = async_crawl_and_index_pipeline.delay(url).id
                    print(f"Crawling task started. Task ID: {task_id}")
                    print("Use the API or Celery CLI to track task status.")
                except Exception as e:
                    print("An error occurred while starting the async task.")
                    logging.error(f"Error in asynchronous crawling: {e}", exc_info=True)

            elif choice == "3":
                # Querying the system
                question = input("Enter your question: ").strip()
                if not question:
                    print("Question cannot be empty. Please try again.")
                    continue
                try:
                    print(f"Querying the system for: {question}")
                    response = run_query_pipeline(question)
                    print(f"\nAnswer: {response}\n")
                except Exception as e:
                    print("An error occurred while processing your query.")
                    logging.error(f"Error in querying pipeline: {e}", exc_info=True)

    except Exception as e:
        logging.critical(f"Critical error in CLI execution: {e}", exc_info=True)
        print("An unexpected error occurred. Please check the logs.")


if __name__ == "__main__":
    main()
