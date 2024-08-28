"""
File: app.py (Automated-Waste-Segregation-System)
Description: This file contains the main algorithm for the Automated Waste Segregation System.

Copyright 2024 STEM Mavericks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = 'Your_secret_key'  # Replace with your own secret key for production use

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
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Basic validation example
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        # Check if the username already exists
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        if not c.fetchone():
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('Registration successful!', 'success')
        else:
            flash('Username already exists!', 'error')
        conn.close()
        return redirect(url_for('login'))

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html')
if __name__ == 'main':
    app.run(debug=True)