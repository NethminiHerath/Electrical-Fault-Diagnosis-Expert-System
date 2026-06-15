import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nethu@9697",
        database="fault_expert_system"
    )


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
    explanation
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
            emergency_load
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        voltage,
        current,
        temperature,
        frequency,
        maintenance_mode,
        emergency_load
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


def get_diagnosis_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            created_at,
            fault_type,
            severity
        FROM diagnosis_history
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows