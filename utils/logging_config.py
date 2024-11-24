import logging


def configure_logging(log_file: str = "app.log", level: int = logging.INFO):
    """
    Configure the logging settings for the application.

    Args:
        log_file (str): Path to the log file.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    logging.info("Logging configuration initialized.")
