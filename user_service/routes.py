from flask import Blueprint, request, jsonify
import requests  # Add this import
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.utils import decode_token
from werkzeug.security import check_password_hash
from models import User
from data import save_users, load_users  # Import the necessary functions
from dotenv import load_dotenv
import os
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
# Load environment variables from .env file
load_dotenv()

user_bp = Blueprint('user', __name__)

# Admin Registration Code from Environment
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","supersecretkey123")
AUTH_SERVICE_URL = "http://127.0.0.1:5002"


# Endpoint: Register a new user
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')  # Default role is "User"
    admin_code = data.get('admin_code', None)
    
    # Validate inputs
    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required!'}), 400

    if not User.is_valid_email(email):
        return jsonify({'error': 'Invalid email format!'}), 400

    if not User.is_valid_password(password):
        return jsonify({'error': 'Password must be at least 5 characters long!'}), 400

    # Load the current users from the file
    #print("Existing users:", load_users())
    users_db = load_users()
    
    # Check if the email is already registered
    if any(user['email'] == email for user in users_db):
        return jsonify({'error': 'Email already registered!'}), 400

    # Check admin code validity by calling the Authentication service
    if role.lower() == 'admin' and admin_code:
        response = requests.post(f"{AUTH_SERVICE_URL}/api/auth/validate_admin_code", json={"admin_code": admin_code})
        if response.status_code == 200:
            new_user = User(name, email, password, role)
            users_db.append(new_user.to_dict())  # Add the new user to the users_db list
            save_users(users_db)  # Save the updated users_db to the file
            return jsonify({'message': 'Admin registered successfully!'}), 201
        else:
            return jsonify({'error': 'Invalid admin code'}), 403
    
    elif role.lower() == 'user' and admin_code:
        return jsonify({'error': 'Role as in User can not be registered as an Admin. '}), 403

    elif role.lower() == 'user':  
        new_user = User(name, email, password, role)
        users_db.append(new_user.to_dict())  
        save_users(users_db)  
        return jsonify({'message': 'User registered successfully!'}), 201   
    else:
        new_user = User(name, email, password, role = "User")
        users_db.append(new_user.to_dict())  
        save_users(users_db)  
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

    users_db = load_users()  # Load the users list from the file
    user = next((user for user in users_db if user['email'] == email), None)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    # Check if the password matches (using hashed password)
    if not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid password"}), 401
    
    role = user.get('role', 'User')
    # Create a JWT token for the user
    #access_token = create_access_token(identity={"email": email, "role": role})
    access_token = create_access_token(identity=email, additional_claims={"role": role})

    

    # Return the token to the client
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
    }), 200



# Endpoint: View Profile
@user_bp.route('/profile', methods=['GET'])
def profile():
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing Authorization header"}), 401

    try:
        # Extract the token from the Authorization header
        token = auth_header.split()[1]
        
        # Send the token to authentication service to decode
        response = requests.post(f"{AUTH_SERVICE_URL}/api/auth/decode_token", json={"token": token})

        if response.status_code != 200:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        decoded_token = response.json()
        current_user_email = decoded_token.get('email')
        role = decoded_token.get('role')

        # Load all users from userdata.py (assuming this loads the list of all users)
        users_db = load_users()

        # Find the user with the matching email
        user = next((u for u in users_db if u['email'] == current_user_email), None)

        if not user:
            return jsonify({"message": "User not found in database"}), 404

        # Return the user's details (including name, email, role, etc.)
        return jsonify({
            "user": {
                "name": user['name'],
                "email": user['email'],
                "role": user['role'],
                # You may choose not to return the password
            }
        }), 200

    except IndexError:
        return jsonify({"message": "Bearer token malformed"}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

