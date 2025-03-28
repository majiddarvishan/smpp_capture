from db import get_db_connection

def store_smpp_data(sequence_number, submit_time, submit_resp_time, source, dest, command_status):
    """Store SMPP packet insights in PostgreSQL"""
    latency_ms = (submit_resp_time - submit_time).total_seconds() * 1000 if submit_resp_time else None

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO smpp_data (sequence_number, submit_time, submit_resp_time, latency_ms, source_addr, destination_addr, command_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (sequence_number) DO UPDATE
        SET submit_resp_time = EXCLUDED.submit_resp_time,
            latency_ms = EXCLUDED.latency_ms,
            command_status = EXCLUDED.command_status;
    """, (sequence_number, submit_time, submit_resp_time, latency_ms, source, dest, command_status))

    conn.commit()
    cur.close()
    conn.close()
