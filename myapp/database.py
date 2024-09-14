from app import app, db

def create_database():
    with app.app_context():
        # Create the database and tables
        db.create_all()
        print("Database created and tables initialized.")

if __name__ == "__main__":
    create_database()
