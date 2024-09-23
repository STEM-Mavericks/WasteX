from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_mail import Mail
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OAuth Config For GitHub
app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')

# Email Config
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# Initialize extensions
mail = Mail(app)
oauth = OAuth(app)
db = SQLAlchemy(app)

# OAuth GitHub setup
github = oauth.register(
    'github',
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRET'],
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Database models
class WasteData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    dry_waste = db.Column(db.Float, nullable=False, default=0)
    wet_waste = db.Column(db.Float, nullable=False, default=0)
    weight = db.Column(db.Float, nullable=False, default=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ManualEntryForm(FlaskForm):
    dry_waste = FloatField('Dry Waste (kg)', validators=[DataRequired()])
    wet_waste = FloatField('Wet Waste (kg)', validators=[DataRequired()])
    weight = FloatField('Total Weight (kg)', validators=[DataRequired()])
    submit = SubmitField('Submit Data')

# Routes
@app.route('/')
def index():
    waste_data = WasteData.query.all()
    total_dry = sum(data.dry_waste for data in waste_data)
    total_wet = sum(data.wet_waste for data in waste_data)
    total_weight = sum(data.weight for data in waste_data)
    return render_template('dashboard.html', waste_data=waste_data, total_dry=total_dry, total_wet=total_wet, total_weight=total_weight)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/manual_entry', methods=['GET', 'POST'])
def manual_entry():
    form = ManualEntryForm()
    if form.validate_on_submit():
        new_data = WasteData(dry_waste=form.dry_waste.data, wet_waste=form.wet_waste.data, weight=form.weight.data)
        db.session.add(new_data)
        db.session.commit()
        flash('Data added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('manual_entry.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/github/login')
def github_login():
    redirect_uri = url_for('authorized', _external=True)
    return github.authorize(redirect_uri=redirect_uri)

@app.route('/github/callback')
def authorized():
    token = github.authorize_access_token()
    user_info = github.get('user')
    session['github_user'] = user_info.json()
    flash('You are now logged in with GitHub!', 'success')
    return redirect(url_for('index'))

# Initialize database and run app
if __name__ == '__main__':
    app.run(debug=True)
