from flask import Blueprint, request, jsonify, render_template
from .models import db, WasteData, User

bp = Blueprint('routes', __name__)

@bp.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(f"Received data: {data}")
    
    waste_data = WasteData(data=data['data'])
    db.session.add(waste_data)
    db.session.commit()

    return jsonify({"message": "Data received successfully"}), 200

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/analytics')
def analytics():
    return render_template('analytics.html')
