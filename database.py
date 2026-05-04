import sqlite3
import os

DB_NAME = "northshore.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouses (
        warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        sender_name TEXT NOT NULL,
        receiver_name TEXT NOT NULL,
        receiver_address TEXT NOT NULL,
        item_description TEXT NOT NULL,
        delivery_status TEXT DEFAULT 'Pending',
        assigned_driver TEXT,
        route_details TEXT,
        delivery_date TEXT,
        transport_cost REAL DEFAULT 0.0,
        surcharge REAL DEFAULT 0.0,
        payment_status TEXT DEFAULT 'Unpaid'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        warehouse_id INTEGER,
        quantity INTEGER NOT NULL,
        reorder_level INTEGER NOT NULL,
        location TEXT,
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_number TEXT UNIQUE NOT NULL,
        capacity TEXT NOT NULL,
        maintenance_date TEXT,
        availability TEXT DEFAULT 'Available'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        license_number TEXT NOT NULL,
        phone TEXT,
        shift_assignment TEXT,
        route_history TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shipment_id INTEGER,
        incident_type TEXT NOT NULL,
        description TEXT NOT NULL,
        reported_date TEXT NOT NULL,
        resolution_status TEXT DEFAULT 'Open',
        FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")