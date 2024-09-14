from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

def add_confirmed_column():
    with app.app_context():
        # Execute raw SQL to add the 'confirmed' column
        with db.engine.connect() as connection:
            connection.execute(
                'ALTER TABLE user ADD COLUMN confirmed BOOLEAN NOT NULL DEFAULT 0;'
            )
        print("Column 'confirmed' added to 'user' table.")

if __name__ == '__main__':
    add_confirmed_column()
