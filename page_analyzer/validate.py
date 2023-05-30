from urllib.parse import urlparse
import validators
from page_analyzer.db import get_url_name


def validate_url(url) -> dict:
    """Validate the entered URL address.

    Args:
        url (str): The URL address to validate.

    Returns:
        dict: A dictionary containing the validated URL and any errors found.

    """
    try:
        if len(url) == 0:
            raise ValueError('URL is empty')
        elif len(url) > 255:
            raise ValueError('URL exceeds maximum length')
        elif not validators.url(url):
            raise ValueError('URL is invalid')
    except ValueError as e:
        return {'url': url, 'error': str(e)}

    return {'url': url, 'error': None}


def process_url(url):
    """Process the URL by removing unnecessary parts."""
    url = urlparse(url)
    url = f'{url.scheme}://{url.netloc}'
    return url


def check_url_exists(url):
    """Check if the URL already exists in the database."""
    found = get_url_name(url)
    return found is not None


def validate_and_process_url(url) -> dict:
    """Validate and process the entered URL address.

    Args:
        url (str): The URL address to validate and process.

    Returns:
        dict: A dictionary containing the validated and processed URL 
        and any errors found.

    """
    validation_result = validate_url(url)
    if validation_result['error'] is None:
        url = process_url(url)
        if check_url_exists(url):
            validation_result['error'] = 'exists'

    return validation_result

