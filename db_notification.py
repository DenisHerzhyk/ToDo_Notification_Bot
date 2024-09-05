import sqlite3

def db_connection():
    conn = sqlite3.connect("main.db")
    conn.row_factory = sqlite3.Row
    return conn


def db_get_all_notifications():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications")
    notifications = cursor.fetchall()
    conn.close()
    return notifications


def db_get_notification_by_id(notification_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications WHERE id=?", (notification_id,))
    curr_notification = cursor.fetchone()
    conn.close()
    return curr_notification


def db_insert_notification(title, description, year, month, day, hours, minutes):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (title, description, year, month, day, hours, minutes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, description, year, month, day, hours, minutes))
    conn.commit()
    conn.close()

def db_delete_notification(notification_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notifications WHERE id=?", (notification_id,))
    conn.commit()
    conn.close()