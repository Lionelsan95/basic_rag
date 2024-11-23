import redis
import hashlib
import logging

# Connect to Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

def hash_url(url: str) -> str:
    """Create a unique hash for a URL."""
    return hashlib.sha256(url.encode()).hexdigest()

def is_url_scraped(url: str) -> bool:
    """
    Check if a URL has already been scraped.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is already scraped, False otherwise.
    """
    key = hash_url(url)
    is_scraped = redis_client.exists(key)
    logging.info(f"Checked URL '{url}' - Scraped: {is_scraped}")
    return is_scraped

def mark_url_as_scraped(url: str, ttl: int = None):
    """
    Mark a URL as scraped by adding it to Redis.

    Args:
        url (str): The URL to mark.
        ttl (int): Optional TTL (time-to-live) in seconds for the key.
    """
    key = hash_url(url)
    redis_client.set(key, "scraped", ex=ttl)
    logging.info(f"Marked URL '{url}' as scraped with TTL: {ttl}")
