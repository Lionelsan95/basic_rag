from generation.generate import query_llm
from utils.web_checkers import is_valid_url
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_user_name() -> str:
    """Prompt the user for their name."""
    name = input("What is your name? ")
    logging.info(f"User name: {name}")
    return name


def get_source_url(name: str) -> str:
    """Prompt the user for a valid website URL."""
    while True:
        source_url = input(
            f"{name}, please enter a website URL as the source for our discussion: \n"
        )
        if is_valid_url(source_url):
            logging.info(f"Source URL validated: {source_url}")
            return source_url
        print("Sorry, that URL is not valid.")
        logging.warning("Invalid URL entered.")


def chat_loop(name: str, source_url: str):
    """Main chat loop where user can query the LLM."""
    print(f"Nice to meet you, {name}! How can I help you?")
    logging.info("Starting chat loop.")
    try:
        while True:
            question = input(f"\n{name}: ")
            response = query_llm(source_website_url=source_url, question=question)
            print(f"\nSystem: \n{response}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        logging.info("User terminated the chat.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)


def main():
    """Entry point for the CLI application."""
    print("==> Local Basic RAG <==")
    user_name = get_user_name()
    source_url = get_source_url(user_name)
    chat_loop(user_name, source_url)


if __name__ == "__main__":
    main()
