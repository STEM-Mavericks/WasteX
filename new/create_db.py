from app import app, db

def create_db():
    with app.app_context():
        db.create_all()
        print("Database created and tables created")

if __name__ == '__main__':
    create_db()
