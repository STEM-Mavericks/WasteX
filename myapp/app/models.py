from myapp import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class WasteData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=db.func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
