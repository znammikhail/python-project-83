from dotenv import load_dotenv
import psycopg2
import os
from psycopg2.extras import RealDictCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def create_connection():
    return psycopg2.connect(DATABASE_URL)


def get_urls():
    """
    Retrieve a list of URLs and their latest check status from the database.

    Returns:
        A list of tuples containing the
        URL ID, name, last check timestamp, and status code.
    """
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute('''SELECT urls.id,
                        urls.name,
                        MAX(url_checks.created_at) AS last_check,
                        url_checks.status_code
                    FROM urls
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id
                    GROUP BY urls.id, urls.name, url_checks.status_code
                    ''')
        urls = cur.fetchall()
    conn.close()
    return urls


def get_url_by_id(id) -> dict:
    """
    Get a URL by its ID from the database.

    Args:
        id (int): The ID of the URL.

    Returns:
        Returns:
        dict:   - 'id': The ID of the URL.
                - 'name': The name of the URL.
    """
    conn = create_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        url = cur.fetchone()
    conn.close()
    return url


def get_url_by_name(name) -> dict:
    """
    Get a URL from the database by its name.

    Args:
        name (str): The name of the URL to retrieve.

    Returns:
        dict:   - 'id': The ID of the URL.
                - 'name': The name of the URL.
    """
    conn = create_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
        url = cur.fetchone()
    conn.close()
    return url


def add_url_to_db(url, created_at):
    """
    Adds a new URL to the database with the given name and creation date.

    Args:
        url (str): The name of the URL to add.
        created_at (str): The creation date.

    Returns:
        None.
    """
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
            (url, created_at),
        )
        conn.commit()
    conn.close()


def add_check_to_db(url_id, status_code, h1, title, description, created_at):
    """
    Add a new URL check to the database.

    Args:
        url_id (int): ID of the URL being checked.
        status_code (int): HTTP status code returned by the server.
        h1 (str): The value of the first <h1> tag on the page.
        title (str): The title of the page.
        description (str): The meta description of the page.
        created_at (str): Timestamp of when the check was performed.
    """
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO
            url_checks (url_id,
                        status_code,
                        h1,
                        title,
                        description,
                        created_at)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (url_id, status_code, h1, title, description, created_at),
        )
        conn.commit()
    conn.close()


def get_check(url_id):
    """
    Retrieve a list of check results for a given URL from the database.

    Args:
        url_id (int): The ID of the URL to retrieve check results for.

    Returns:
        id, url_id, status_code, h1, title, description, created_at.
    """
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(
            '''SELECT * FROM url_checks
            WHERE url_id=(%s) ORDER BY id DESC''',
            (url_id,))
        url_list = cur.fetchall()
    conn.close()
    return url_list
