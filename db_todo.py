import sqlite3


def db_connection():
    conn = sqlite3.connect("main.db")
    conn.row_factory = sqlite3.Row
    return conn


def db_get_all_lists():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_lists")
    lists = cursor.fetchall()
    conn.close()
    return lists


def db_insert_and_display_lists(todo_name):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo_lists (name) VALUES (?)", (todo_name,))
    conn.commit()
    cursor.execute("SELECT * FROM todo_lists")
    lists = cursor.fetchall()
    conn.close()
    return lists


def db_delete_and_display_lists(list_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo_lists WHERE id=?", (list_id,))
    conn.commit()
    cursor.execute("SELECT * FROM todo_lists")
    lists = cursor.fetchall()
    conn.close()
    return lists


def db_get_tasks_by_id(list_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_tasks WHERE list_id=?", (list_id,))
    tasksall = cursor.fetchall()
    conn.close()
    return tasksall


def db_get_list_name_by_id(list_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_lists WHERE id=?", (list_id,))
    list_name = cursor.fetchone()['name']
    return list_name


def db_get_task_status(task_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, name FROM todo_tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task



def db_update_task_status(task_id, new_status):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE todo_tasks SET status=? WHERE id=?", (new_status, task_id))
    conn.commit()
    conn.close()

def db_insert_and_display_tasks(list_id, task_name):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo_tasks (list_id, name) VALUES (?, ?)", (list_id, task_name))
    conn.commit()
    cursor.execute("SELECT * FROM todo_tasks WHERE list_id=?", (list_id,))
    tasksall = cursor.fetchall()
    conn.close()
    return tasksall


def db_delete_and_display_task(list_id, task_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo_tasks WHERE list_id=? AND id=?", (list_id, task_id))
    conn.commit()

    cursor.execute("SELECT * FROM todo_tasks WHERE list_id=?", (list_id,))
    tasksall = cursor.fetchall()
    conn.close()
    return tasksall