import sqlite3

conn = sqlite3.connect("main.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS todo_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
''')

cursor.execute('''
    
    CREATE TABLE IF NOT EXISTS todo_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        list_id INTEGER,
        name TEXT NOT NULL,
        status INTEGER DEFAULT 0,
        FOREIGN KEY (list_id) REFERENCES todo_lists (id) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT NOT NULL,
        year INTEGER,
        month INTEGER,
        day INTEGER, 
        hours INTEGER,
        minutes INTEGER
    )
''')

conn.commit()
conn.close()
