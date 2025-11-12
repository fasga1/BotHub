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
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT full_name FROM employees ORDER BY full_name")
            return [row['full_name'] for row in cur.fetchall()]
    finally:
        conn.close()

def verify_community_manager(email: str, password: str) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT 1 FROM community_managers WHERE email = %s AND password_hash = %s",
                (email, password)
            )
            return cur.fetchone() is not None
    finally:
        conn.close()