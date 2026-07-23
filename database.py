import os

import mysql.connector


def _ensure_optional_reading_columns(conn):
    """Add newer input columns to databases created by the original schema."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = 'readings'
    """)
    columns = {row[0] for row in cursor.fetchall()}
    missing = []
    if "current_fluctuation" not in columns:
        missing.append("ADD COLUMN current_fluctuation BOOLEAN NOT NULL DEFAULT FALSE")
    if "voltage_fluctuation" not in columns:
        missing.append("ADD COLUMN voltage_fluctuation BOOLEAN NOT NULL DEFAULT FALSE")
    if missing:
        cursor.execute("ALTER TABLE readings " + ", ".join(missing))
        conn.commit()
    cursor.close()


def get_connection():
    password = os.getenv("RBES_DB_PASSWORD")
    if not password:
        raise RuntimeError("RBES_DB_PASSWORD is not set. Configure the database password before starting the application.")

    conn = mysql.connector.connect(
        host=os.getenv("RBES_DB_HOST", "localhost"),
        user=os.getenv("RBES_DB_USER", "root"),
        password=password,
        database=os.getenv("RBES_DB_NAME", "fault_expert_system")
    )
    _ensure_optional_reading_columns(conn)
    return conn


def save_diagnosis(
    voltage,
    current,
    temperature,
    frequency,
    maintenance_mode,
    emergency_load,
    diagnosis,
    severity,
    actions,
    explanation,
    current_fluctuation=False,
    voltage_fluctuation=False
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO readings
        (
            voltage,
            current_value,
            temperature,
            frequency_value,
            maintenance_mode,
            emergency_load,
            current_fluctuation,
            voltage_fluctuation
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        voltage,
        current,
        temperature,
        frequency,
        maintenance_mode,
        emergency_load,
        current_fluctuation,
        voltage_fluctuation
    ))

    reading_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO diagnosis_history
        (
            reading_id,
            fault_type,
            severity,
            action_taken,
            explanation
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        reading_id,
        diagnosis,
        severity,
        actions,
        explanation
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_diagnosis_history(search_term=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT created_at, fault_type, severity
        FROM diagnosis_history
    """
    if search_term:
        query += " WHERE fault_type LIKE %s OR severity LIKE %s OR action_taken LIKE %s"
        value = f"%{search_term}%"
        cursor.execute(query + " ORDER BY created_at DESC", (value, value, value))
    else:
        cursor.execute(query + " ORDER BY created_at DESC")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
