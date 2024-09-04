from flask import render_template, redirect, url_for, flash
from . import app
from .models import db, User
from flask import request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():

        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    
        return render_template('register.html')

@app.route('/analytics')
def analytics():
     return render_template('analytics.html')

@app.route('/error')
def error():
     return render_template('error.html')