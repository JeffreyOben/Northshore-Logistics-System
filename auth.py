from database import get_connection
from security import hash_password


def create_admin():
    conn = get_connection()
    cursor = conn.cursor()

    username = "admin"
    password = hash_password("admin123")
    role = "Admin"
    full_name = "System Administrator"

    try:
        cursor.execute("""
        INSERT INTO users (username, password, role, full_name)
        VALUES (?, ?, ?, ?)
        """, (username, password, role, full_name))

        conn.commit()
        print("Admin user created successfully.")

    except:
        print("Admin already exists.")

    conn.close()


if __name__ == "__main__":
    create_admin()