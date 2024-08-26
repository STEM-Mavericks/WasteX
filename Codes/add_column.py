import sqlite3

def add_missing_column():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Add the missing column
    cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT;")
    conn.commit()
    conn.close()

add_missing_column()
