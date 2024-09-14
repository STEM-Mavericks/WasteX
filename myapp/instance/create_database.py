from myapp import create_app
from myapp.models import db

# Initialize the Flask application
app = create_app()

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database created successfully.")
