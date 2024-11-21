from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, users_db, save_users
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
import json
import os
user_bp = Blueprint('user', __name__)

# Endpoint: Register a new user
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')  # Default role is "User"

    # Validate inputs
    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required!'}), 400

    if not User.is_valid_email(email):
        return jsonify({'error': 'Invalid email format!'}), 400

    if not User.is_valid_password(password):
        return jsonify({'error': 'Password must be at least 5 characters long!'}), 400

    # Check if the user already exists
    if User.find_by_email(email):
        return jsonify({'error': 'Email already registered!'}), 400

    # Create and save user
    new_user = User(name, email, password, role)
    users_db.append(new_user.to_dict())
    save_users(users_db)  # Save users to file
    return jsonify({'message': 'User registered successfully!'}), 201

# Endpoint: Login
@user_bp.route('/login', methods=['POST'])
def login():
    # Get the request data (email and password)
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Read user data from the JSON file
    try:
        with open(os.path.join(os.path.dirname(__file__), 'users.json'), 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        return jsonify({"message": "No users found, please register first"}), 404

    # Search for the user by email
    user = next((user for user in users if user['email'] == email), None)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    # Check if the password matches (using hashed password)
    if not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid password"}), 401

    # Create a JWT token for the user
    access_token = create_access_token(identity=email)

    # Return the token to the client
    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    email = get_jwt_identity()  # Just get the email directly

    # Find user by email
    user = User.find_by_email(email)
    if not user:
        return jsonify({'error': 'User not found!'}), 404

    # Return user profile
    return jsonify({'name': user['name'], 'email': user['email'], 'role': user['role']}), 200
