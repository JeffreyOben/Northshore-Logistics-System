from database import get_connection
from datetime import datetime


def log_activity(username, action):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO activity_logs (username, action, timestamp)
            VALUES (?, ?, ?)
        """, (username, action, datetime.now()))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Logging failed:", e)