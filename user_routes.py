from flask import Blueprint, request, jsonify

user_blueprint = Blueprint('user', __name__)

# Mock user database
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]


@user_blueprint.route('/list', methods=['GET'])
def list_users():
    """Returns a list of users"""
    return jsonify(users)


@user_blueprint.route('/add', methods=['POST'])
def add_user():
    """Adds a new user"""
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing name or email"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201


@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Fetch a single user by ID"""
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404
