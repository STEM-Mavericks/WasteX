from app import db
from app.models import User

db.create_all()

print("Database created successfully!")