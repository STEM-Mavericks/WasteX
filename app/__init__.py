from flask import Flask
from .models import db

def create_app():
 app = Flask(__name__)
 app.config.from_object('config.Config')

 db.init_app(app)

 with app.app_context():
  from . import routes

  db.create_all()

  return app