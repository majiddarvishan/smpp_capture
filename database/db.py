import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
import time
from config.config import POSTGRES_CONFIG
from database.queries import create_tables

# Create a connection pool (min 1, max 10 connections)
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        **POSTGRES_CONFIG
    )
    print("✅ PostgreSQL connection pool created successfully.")
except psycopg2.Error as e:
    print(f"❌ Error creating PostgreSQL connection pool: {e}")
    connection_pool = None


def get_db_connection():
    """Gets a connection from the pool, retries on failure."""
    retries = 3
    delay = 2  # seconds

    for attempt in range(retries):
        if connection_pool:
            try:
                conn = connection_pool.getconn()
                if conn:
                    return conn
            except psycopg2.Error as e:
                print(f"⚠️ Database connection failed (attempt {attempt + 1}): {e}")
                time.sleep(delay)

    print("❌ Failed to connect to the database after multiple attempts.")
    return None


def release_connection(conn):
    """Releases the connection back to the pool."""
    if conn and connection_pool:
        connection_pool.putconn(conn)


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
            release_connection(conn)


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Executes a SQL query with automatic reconnection handling."""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor(cursor_factory=DictCursor)
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
    except psycopg2.OperationalError as e:
        print(f"⚠️ Lost connection to database, retrying...: {e}")
        return execute_query(query, params, fetch_one, fetch_all)
    except psycopg2.Error as e:
        print(f"❌ Query Execution Error: {e}")
        return None
    finally:
        release_connection(conn)
