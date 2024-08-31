from . import db

class WasteData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waste_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<WasteData {self.waste_type} {self.weight}kg>'