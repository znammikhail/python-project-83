from dotenv import load_dotenv
import psycopg2
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
        cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
        urls = cur.fetchall()
    # Закрытие курсора и соединения с базой данных
    conn.close()
    return urls


def get_url_id(id):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        url = cur.fetchone()
        print(url)
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
