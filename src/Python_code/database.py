import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def get_all_employees():
    return [
        "Анна Петрова",
        "Иван Смирнов",
        "Мария Козлова",
        "Алексей Иванов",
        "Екатерина Соколова",
        "Ольга Новикова"  # ← можно добавлять сколько угодно
    ]
    #conn = get_db_connection()
    #try:
    #    with conn.cursor(cursor_factory=RealDictCursor) as cur:
    #        cur.execute("SELECT full_name FROM employees ORDER BY full_name")
    #        return [row['full_name'] for row in cur.fetchall()]
    #finally:
    #    conn.close()