from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.config')

db = SQLAlchemy(app)

from .routes import main_bp
app.register_blueprint(main_bp)

def init_db():
    db.create_all()

