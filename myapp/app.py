from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta  # Added timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configurations
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenviron.get('DATABASE_URL')
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)
serializer = Serializer(app.config['SECRET_KEY'])

# User model and token methods
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    otp = db.Column(db.String(6), nullable=True)  # New field for OTP
    otp_expiry = db.Column(db.DateTime, nullable=True)  # New field for OTP expiry
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_reset_token(self, expires_sec=3600):
        return serializer.dumps({'user_id': self.id}, salt='password-reset-salt')
    
    @staticmethod
    def verify_reset_token(token, expires_sec=3600):
        try:
            user_id = serializer.loads(token, salt='password-reset-salt', max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def get_confirmation_token(self, expires_sec=3600):
        return serializer.dumps({'user_id': self.id}, salt='confirm-email-salt')
    
    @staticmethod
    def verify_confirmation_token(token, expires_sec=3600):
        try:
            user_id = serializer.loads(token, salt='confirm-email-salt', max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def generate_otp(self):
        """Generate a 6-digit OTP and set its expiry time."""
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()
    
    def verify_otp(self, otp):
        """Verify the OTP entered by the user."""
        if self.otp == otp and datetime.utcnow() < self.otp_expiry:
            self.otp = None  # Clear OTP after verification
            self.otp_expiry = None
            self.confirmed = True
            db.session.commit()
            return True
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# Email functions
def send_confirmation_email(user):
    token = user.get_confirmation_token()
    msg = Message('Confirm Your Email', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[user.email])
    msg.body = f'''To confirm your account, visit the following link:
{url_for('confirm_email', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

def send_otp_email(user):
    otp = user.otp
    msg = Message('Confirm Your Email with OTP', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[user.email])
    msg.body = f'''To confirm your account, use the following OTP:
{otp}

This OTP will expire in 10 minutes. If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user.generate_otp()  # Generate OTP
        send_otp_email(user)  # Send OTP email
        flash('Your account has been created! Please check your email for OTP to confirm your account.', 'success')
        return redirect(url_for('verify_otp', user_id=user.id))
    return render_template('register.html', form=form)

@app.route('/verify-otp/<int:user_id>', methods=['GET', 'POST'])
def verify_otp(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        otp = request.form.get('otp')
        if user.verify_otp(otp):
            flash('Your email has been confirmed!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired OTP', 'danger')
    return render_template('verify_otp.html', user=user)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_confirmation_token(token)
    if user:
        user.confirmed = True
        db.session.commit()
        flash('Your email has been confirmed!', 'success')
        return redirect(url_for('login'))
    else:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('index'))

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('No account found with that email address.', 'danger')
    return render_template('reset_request.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
