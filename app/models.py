from . import db

# WasteData model
class WasteData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waste_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<WasteData {self.waste_type} {self.weight}kg>'

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
