import re
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Validates a URL for proper structure and accessibility.
    :param url: The URL to validate.
    :return: True if valid, False otherwise.
    """
    # Basic URL regex for initial validation
    regex = re.compile(
        r"^(https?|ftp)://"  # Scheme
        r"([a-zA-Z0-9.-]+)"  # Domain
        r"(:[0-9]{1,5})?"  # Optional port
        r"(\/.*)?$"  # Optional path/query
    )

    if not regex.match(url):
        return False

    # Parse and check the structure of the URL
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except Exception:
        return False
