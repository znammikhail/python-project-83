from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def create_connection():
    return psycopg2.connect(DATABASE_URL)


def get_urls() -> dict:
    # Создание соединения с базой данных PostgreSQL
    conn = create_connection()
    # Создание курсора для работы с базой данных
    with conn.cursor() as cur:
        # Выполнение SQL-запроса для получения всех URL адресов, отсортированных по дате создания в обратном порядке
        cur.execute('''SELECT urls.id, urls.name,
                    MAX(url_checks.created_at) AS last_check
                    FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id 
                    GROUP BY urls.id, urls.name;''')
        urls = cur.fetchall()
    # Закрытие курсора и соединения с базой данных
    conn.close()
    return urls


def get_url_id(id):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        url = cur.fetchone()
    conn.close()
    return url


def get_url_name(name):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
        url = cur.fetchone()
    conn.close()
    return url


def add_url_db(url, created_at):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
            (url, created_at),
        )
        conn.commit()
    conn.close()


def add_check_db(url_id, created_at):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)",
            (url_id, created_at),
        )
        conn.commit()
    conn.close()


def get_check_db(url_id):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC", (url_id,))
        url_list = cur.fetchall()
    conn.close()
    return url_list
