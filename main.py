import logging
from pipelines.rag_pipeline import run_rag_pipeline
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
        # Step 1: Get user name
        user_name = input("What is your name? ").strip()
        if not user_name:
            raise ValueError("Name cannot be empty.")
        logging.info(f"User name: {user_name}")

        while True:
            # Step 2: Prompt for website URL
            url = input(f"{user_name}, enter a website URL to scrape (or type 'exit'): ").strip()
            if url.lower() in {"exit", "quit"}:
                print("Goodbye!")
                logging.info("User exited the CLI.")
                break
            if not is_valid_url(url):
                print("Invalid URL. Please try again.")
                logging.warning(f"Invalid URL entered: {url}")
                continue

            # Step 3: Prompt for user question
            question = input(f"{user_name}, what would you like to ask? ").strip()
            if question.lower() in {"exit", "quit"}:
                print("Goodbye!")
                logging.info("User exited the CLI.")
                break

            # Step 4: Run the RAG pipeline
            try:
                print(f"Processing your query using the RAG pipeline for {url}...")
                response = run_rag_pipeline(url, question)
                print(f"\nAnswer: {response}\n")
            except Exception as e:
                print("An error occurred while processing your query. Please try again.")
                logging.error(f"Error in RAG pipeline execution: {e}", exc_info=True)

    except Exception as e:
        logging.critical(f"Critical error in CLI execution: {e}", exc_info=True)
        print("An unexpected error occurred. Please check the logs.")

if __name__ == "__main__":
    main()
