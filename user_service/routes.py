from flask import Blueprint, request, jsonify
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
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE", "Syeda_Samia_Sultana")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","supersecretkey123")

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
    print("Existing users:", load_users())
    users_db = load_users()
    
    # Check if the email is already registered
    if any(user['email'] == email for user in users_db):
        return jsonify({'error': 'Email already registered!'}), 400

    # Check for admin registration code if the role is "Admin"
    if role.lower() == 'admin' and admin_code != ADMIN_REGISTRATION_CODE:
        return jsonify({'error': 'Invalid or missing admin registration code!'}), 403

    # Create and save the user
    new_user = User(name, email, password, role)
    users_db.append(new_user.to_dict())  # Add the new user to the users_db list

    # Save the updated users_db to the file
    save_users(users_db)

    # Return a success message based on the role
    if role.lower() == 'admin':
        return jsonify({'message': 'Admin registered successfully!'}), 201
    else:
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

        # Decode the JWT token
        decoded_token = decode_token(token)

        # Access the user's identity (email) and role from the token
        current_user_email = decoded_token.get('sub')  # 'sub' is the identity field
        role = decoded_token.get('role')  # Retrieve the additional claim

        # Load all users from userdata.py
        users_db = load_users()  # Assuming this loads the list of all users

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
                "password": user['password']
            }
        }), 200

    except IndexError:
        return jsonify({"message": "Bearer token malformed"}), 400
    except ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except DecodeError:
        return jsonify({"message": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

