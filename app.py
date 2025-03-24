from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)


# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]  # 5 requests per minute as default
)
# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    file_path = db.Column(db.String(200), nullable=True)

# Routes
@app.route('/submit_request', methods=['POST'])
@limiter.limit("3 per minute")
def submit_request():
    data = request.form
    file = request.files.get('file')
    user = User.query.get(data.get('user_id'))

    if not user:
        return jsonify({'error': 'User not found'}), 404

    file_path = None
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    new_request = ServiceRequest(
        user_id=user.id,
        request_type=data.get('request_type'),
        description=data.get('description'),
        file_path=file_path
    )
    db.session.add(new_request)
    db.session.commit()
    
    return jsonify({'message': 'Service request submitted successfully'}), 201

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    # Create new user
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully', 'user_id': new_user.id}), 201


@app.route('/track_request/<int:request_id>', methods=['GET'])
@limiter.limit("10 per minute")
def track_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'error': 'Request not found'}), 404

    return jsonify({
        'request_type': service_request.request_type,
        'status': service_request.status,
        'created_at': service_request.created_at,
        'resolved_at': service_request.resolved_at
    })

# Initialize DB
with app.app_context():
    db.create_all()


# Run App
if __name__ == '__main__':
    app.run(debug=True)
