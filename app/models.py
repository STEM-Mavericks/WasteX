from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WasteData(db.Model):
    __tablename__ = 'waste_data'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
