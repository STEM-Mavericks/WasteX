from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

def add_columns():
    with app.app_context():
        try:
            with db.engine.connect() as connec
            print("Columns 'otp' and 'otp_expiry' added to 'user' table.")
        except OperationalError as e:
            # Handle the case where the column already exists or other issues
            print(f"OperationalError: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    add_columns()
