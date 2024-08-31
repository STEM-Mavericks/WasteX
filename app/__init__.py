from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.config')

db = SQLAlchemy(app)

from .routes import main_bp
app.register_blueprint(main_bp)

def init_db():
    db.create_all()

import logging
from logging.handlers import RotatingFileHandler
if not app.debug:
    file_handler = RotatingFileHandler('log/error.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run(debug=True)