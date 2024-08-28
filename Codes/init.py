import sqlite3

def create_database():
    """Create the database and the users table if it does not exist."""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create the users table with the correct schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

    print('Database data.db is established successfully!')

if __name__ == "__main__":
    create_database()
