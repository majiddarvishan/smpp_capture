def create_tables():
    """Creates necessary tables for storing SMPP data."""
    return """
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
    """


def insert_smpp_data():
    """Insert a new SMPP packet entry or update an existing one."""
    return """
    INSERT INTO smpp_data (sequence_number, submit_time, submit_resp_time, latency_ms, source_addr, destination_addr, command_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (sequence_number) DO UPDATE
    SET submit_resp_time = EXCLUDED.submit_resp_time,
        latency_ms = EXCLUDED.latency_ms,
        command_status = EXCLUDED.command_status;
    """


def update_command_status():
    """Updates the command status for a specific sequence number."""
    return """
    UPDATE smpp_data
    SET command_status = %s
    WHERE sequence_number = %s;
    """


def get_latency_by_sequence():
    """Fetch latency details for a given sequence number."""
    return """
    SELECT sequence_number, submit_time, submit_resp_time, latency_ms
    FROM smpp_data
    WHERE sequence_number = %s;
    """


def get_high_latency_records():
    """Retrieve messages with latency above a specified threshold."""
    return """
    SELECT * FROM smpp_data
    WHERE latency_ms > %s
    ORDER BY latency_ms DESC
    LIMIT 100;
    """


def get_low_latency_records():
    """Retrieve messages with latency below a specified threshold."""
    return """
    SELECT * FROM smpp_data
    WHERE latency_ms < %s
    ORDER BY latency_ms ASC
    LIMIT 100;
    """


def count_high_latency():
    """Count the number of packets with latency greater than the average latency."""
    return """
    SELECT COUNT(*) FROM smpp_data
    WHERE latency_ms > (SELECT AVG(latency_ms) FROM smpp_data);
    """


def count_low_latency():
    """Count the number of packets with latency lower than the average latency."""
    return """
    SELECT COUNT(*) FROM smpp_data
    WHERE latency_ms < (SELECT AVG(latency_ms) FROM smpp_data);
    """


def get_failed_messages():
    """Retrieve messages with non-zero command_status (indicating errors)."""
    return """
    SELECT * FROM smpp_data
    WHERE command_status > 0
    ORDER BY command_status DESC
    LIMIT 100;
    """


def get_latest_records():
    """Retrieve the latest 100 SMPP transactions."""
    return """
    SELECT * FROM smpp_data
    ORDER BY submit_time DESC
    LIMIT 100;
    """


def get_latency_distribution():
    """Get the distribution of latency values for analysis."""
    return """
    SELECT
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms) AS median_latency,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) AS p95_latency,
        PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) AS p99_latency
    FROM smpp_data;
    """


def delete_old_records():
    """Delete records older than a specific timestamp to manage storage."""
    return """
    DELETE FROM smpp_data
    WHERE submit_time < NOW() - INTERVAL '30 days';
    """
