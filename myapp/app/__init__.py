from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Flask-Login configurations
login_manager.login_view = 'login'  # Route name for login view
login_manager.login_message_category = 'info'  # Flash category for login messages

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes (to avoid circular imports)
from app import routes

def create_app():
    with app.app_context():
        db.create_all()
    return app
