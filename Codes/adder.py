import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def update_existing_users():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Update existing users with a default password or handle as needed
    cursor.execute("SELECT username FROM users WHERE password_hash IS NULL")
    users = cursor.fetchall()
    
    for user in users:
        default_password = 'default_password'  # Replace with a proper method to handle existing users
        hashed_password = bcrypt.generate_password_hash(default_password).decode('utf-8')
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hashed_password, user[0]))

    conn.commit()
    conn.close()

update_existing_users()
