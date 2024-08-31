from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint('main.bp', __name__)

@main_bp.route('/')
def index():
    render_template('index.html')

@main_bp.route('/data')
def data():
    render_template('data.html')

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404