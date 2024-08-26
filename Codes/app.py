from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'Your_secret_key'  # Replace with your own secret key

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

DATABASE = 'data.db'

class User(UserMixin):
    def __init__(self, username, password_hash):
        self.id = username  # UserMixin requires an id attribute; this is correctly added here.
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT username, password_hash FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        # Check password complexity
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('register.html')

        if not re.search(r'[A-Z]', password):
            flash('Password must contain at least one uppercase letter.', 'danger')
            return render_template('register.html')

        if not re.search(r'[a-z]', password):
            flash('Password must contain at least one lowercase letter.', 'danger')
            return render_template('register.html')

        if not re.search(r'[0-9]', password):
            flash('Password must contain at least one digit.', 'danger')
            return render_template('register.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            flash('Password must contain at least one special character.', 'danger')
            return render_template('register.html')

        if username and password:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT username FROM users WHERE username=?", (username,))
            if not c.fetchone():
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                conn.close()
                flash('Registration Successful! You can log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists!', 'danger')
                conn.close()
        else:
            flash('Fill out both the details.', 'danger')
        return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = load_user(username)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Password or Username.', 'danger')
        return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html')
