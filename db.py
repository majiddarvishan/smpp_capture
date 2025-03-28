import psycopg2
from psycopg2.extras import DictCursor

# Database config
DB_CONFIG = {
    "dbname": "smpp",
    "user": "user",
    "password": "password",
    "host": "postgres",
    "port": 5432
}

def get_db_connection():
    """Connect to PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=DictCursor)

def setup_tables():
    """Create tables if not exist"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS smpp_data (
        id SERIAL PRIMARY KEY,
        sequence_number BIGINT UNIQUE,
        submit_time TIMESTAMP,
        submit_resp_time TIMESTAMP,
        latency_ms FLOAT,
        source_addr TEXT,
        destination_addr TEXT,
        command_status INT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

# Run table setup
setup_tables()
