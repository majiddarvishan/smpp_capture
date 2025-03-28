import psycopg2
from psycopg2.extras import DictCursor
from config.config import POSTGRES_CONFIG
from database.queries import create_tables


def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG, cursor_factory=DictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None


def initialize_database():
    """Creates necessary tables if they do not exist."""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(create_tables())
            conn.commit()
            cur.close()
            print("✅ Database initialized successfully.")
        except psycopg2.Error as e:
            print(f"❌ Error initializing database: {e}")
        finally:
            conn.close()


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Executes a SQL query and optionally fetches results."""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute(query, params or ())

        if fetch_one:
            result = cur.fetchone()
        elif fetch_all:
            result = cur.fetchall()
        else:
            conn.commit()
            result = None

        cur.close()
        return result
    except psycopg2.Error as e:
        print(f"❌ Query Execution Error: {e}")
        return None
    finally:
        conn.close()
