import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def get_db_connection():
    host = os.getenv("DB_HOST", "localhost")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if host in ["localhost", "127.0.0.1"] or host.startswith("192.168."):
        return psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
    else:
        return psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            sslmode="require"
        )


def get_employees_with_holidays():
    # today = datetime.now().date()
    # today_mm_dd = today.strftime("%m-%d")
    today_mm_dd = "02-23"  # Тестовая дата (23 февраля)

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if today_mm_dd == "12-31":
                cur.execute("""
                    SELECT full_name, 'new_year' AS holiday_type, chat_link
                    FROM employees
                    ORDER BY full_name
                """)
            else:
                cur.execute("""
                    SELECT full_name, 
                           CASE 
                               WHEN TO_CHAR(birthday, 'MM-DD') = %s THEN 'birthday'
                               WHEN %s = '03-08' THEN 'womens_day'
                               WHEN %s = '02-23' THEN 'defender_day'
                           END AS holiday_type,
                           chat_link
                    FROM employees
                    WHERE 
                        (birthday IS NOT NULL AND TO_CHAR(birthday, 'MM-DD') = %s)
                        OR (%s = '03-08' AND gender = 'F')
                        OR (%s = '02-23' AND gender = 'M')
                    ORDER BY full_name
                """, (today_mm_dd, today_mm_dd, today_mm_dd, today_mm_dd, today_mm_dd, today_mm_dd))
            return cur.fetchall()
    finally:
        conn.close()


def verify_community_manager(email: str, password: str) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT 1 FROM community_managers WHERE LOWER(email) = LOWER(%s) AND password_hash = %s",
                (email, password)
            )
            return cur.fetchone() is not None
    finally:
        conn.close()


def email_exists_in_db(email: str) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM community_managers WHERE email = %s",
                (email,)
            )
            return cur.fetchone() is not None
    finally:
        conn.close()


def update_manager_chat_id(email: str, chat_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE community_managers SET chat_id = %s WHERE email = %s",
                (chat_id, email)
            )
            conn.commit()
    finally:
        conn.close()


def get_all_manager_chat_ids():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT chat_id FROM community_managers WHERE chat_id IS NOT NULL")
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()