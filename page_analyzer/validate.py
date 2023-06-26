from urllib.parse import urlparse
import validators
from page_analyzer.db import get_url_by_name


class ValidationResult:
    def __init__(self, url, error=None):
        self.url = url
        self.error = error


def validate_url(url) -> ValidationResult:
    """Validate the entered URL address.

    Args:
        url (str): The URL address to validate.

    Returns:
        ValidationResult: An object containing the validated URL.

    """
    if len(url) == 0:
        return ValidationResult(url, error='URL is empty')
    elif len(url) > 255:
        return ValidationResult(url, error='URL exceeds maximum length')
    elif not validators.url(url):
        return ValidationResult(url, error='URL is invalid')

    return ValidationResult(url, error=None)


def standardize_url(url):
    """Standardize the URL by removing unnecessary parts."""
    parsed_url = urlparse(url)
    standardized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return standardized_url


def is_url_exists(url):
    """Check if the URL already exists in the database."""
    found = get_url_by_name(url)
    return found is not None
