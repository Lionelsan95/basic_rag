from bs4 import BeautifulSoup
import re
import nltk
from langdetect import detect, DetectorFactory

# Download necessary NLTK resources (run once)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Initialize NLTK tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def clean_html_content(html: str) -> str:
    """
    Remove HTML tags and extract meaningful text from raw HTML.

    Args:
        html (str): The raw HTML content.

    Returns:
        str: Cleaned text content.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script, style, and metadata
    for tag in soup(["script", "style", "meta", "noscript"]):
        tag.decompose()

    # Extract plain text
    text = soup.get_text(separator="\n")

    # Normalize spaces and remove excessive newlines
    text = re.sub(r"\s+", " ", text).strip()

    return text

def detect_language(text: str) -> str:
    """
    Detect the language of the text.

    Args:
        text (str): The input text.

    Returns:
        str: Detected language code (e.g., 'en').
    """
    return detect(text)

def preprocess_text(text: str, language: str = "en") -> str:
    """
    Preprocess text: Normalize, remove stopwords, and lemmatize.

    Args:
        text (str): The input text.
        language (str): The language of the text (default: 'en').

    Returns:
        str: Preprocessed text.
    """
    # Normalize case and strip whitespace
    text = text.lower().strip()

    # Tokenize text
    tokens = word_tokenize(text)

    # Remove stopwords and lemmatize tokens
    processed_tokens = [
        lemmatizer.lemmatize(token) for token in tokens
        if token.isalpha() and token not in stop_words
    ]

    return " ".join(processed_tokens)

def filter_quality(text: str, min_length: int = 50) -> bool:
    """
    Filter out low-quality content based on text length.

    Args:
        text (str): The input text.
        min_length (int): Minimum acceptable length of the text.

    Returns:
        bool: True if the content passes the quality filter, False otherwise.
    """
    return len(text) >= min_length
