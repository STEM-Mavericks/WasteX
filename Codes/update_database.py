import sqlite3

def update_database():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Create a new table with the updated schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')

    # Copy data from old table to new table
    cursor.execute('''
        INSERT INTO new_users (username, password_hash)
        SELECT username, password FROM users
    ''')

    # Drop the old table
    cursor.execute('DROP TABLE users')
    
    # Rename the new table to the old table name
    cursor.execute('ALTER TABLE new_users RENAME TO users')

    conn.commit()
    conn.close()

    print('Database schema updated successfully!')

if __name__ == "__main__":
    update_database()
