from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

# Define a blueprint
main_bp = Blueprint('main_bp', __name__)

# Home route
@main_bp.route('/')
def index():
    return render_template('index.html')

# Data route
@main_bp.route('/data')
def data():
    # Logic to retrieve and process data from the database or sensors
    # Example: data = get_sensor_data()
    # For now, we are just passing an empty context
    return render_template('data.html', data={})

# Login route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            # Login success
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_bp.index'))
        else:
            # Login failed
            flash('Login failed. Check your username and password.', 'danger')
    
    return render_template('login.html')

# Register route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('main_bp.register'))
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main_bp.register'))
        
        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main_bp.login'))
    
    return render_template('register.html')

# Error handling
@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
