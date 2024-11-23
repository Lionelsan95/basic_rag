import re

def is_valid_url(url: str) -> bool:
    """
    Validate if a given string is a properly formatted URL.
    
    Args:
        url (str): The URL to validate.
    
    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    url_regex = re.compile(
        r"^(https?://)?"
        r"((([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})|"
        r"localhost|"
        r"(\d{1,3}\.){3}\d{1,3})"
        r"(:\d+)?(/.*)?$"
    )
    return bool(url_regex.match(url))
