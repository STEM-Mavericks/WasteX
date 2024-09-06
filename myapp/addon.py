import sqlite3
import os

# Adjust the path to your SQLite database
db_path = os.path.join('instance', 'site.db')

# Connect to the database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Query to get table information
cursor.execute("PRAGMA table_info(user);")
columns = cursor.fetchall()

# Print column details
for column in columns:
    print(column)

# Close the connection
connection.close()
