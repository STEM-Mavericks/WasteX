from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
import sqlite3

DATABASE = 'data.db'

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, password_hash):
        self.id = username
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

def load_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT username, password_hash FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

@login_manager.user_loader
def user_loader(username):
    return load_user(username)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Your_secret_key'  # Replace with your own secret key

    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
