from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WasteData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=db.func.now())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)