from app import db  # Import the db object from your app module
from app.models import User  # Import your models

def create_database():
    with app.app_context():
        db.create_all()  # Create all tables
        print("Database created and tables initialized.")

if __name__ == "__main__":
    create_database()
