from database import get_connection


def log_activity(username, action):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO activity_logs (username, action)
        VALUES (?, ?)
    """, (username, action))

    conn.commit()
    conn.close()