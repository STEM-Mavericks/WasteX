from app import create_app, db
from app.models import User

# Create an application instance
app = create_app()

# Create the application context
with app.app_context():
    db.create_all()

print("Database created successfully!")
