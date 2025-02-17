from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_blueprint = Blueprint('auth', __name__)

def isValidUser(username, password):
    # This is a mock validation function. Replace it with your actual user validation logic
    return username == 'user@example.com' and password == 'password'

def getUserRole(username):
    # This is a mock function. Replace it with your actual logic to get a user's role
    return 'admin' if username == 'admin@example.com' else 'user'

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if isValidUser(username, password):
        # Adjust 'secretKey' and expiration time as needed
        token = jwt.encode({'username': username, 'role': getUserRole(username), 'exp': datetime.utcnow() + timedelta(hours=1)}, 'secretKey', algorithm="HS256")
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid login'}), 401
