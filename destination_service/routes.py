import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import decode_token
from models import Destination
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()  # This will load the values from .env into environment variables

# Create Blueprint
destination_bp = Blueprint('destination', __name__)

# Get the admin registration code from environment
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE", "Syeda_Samia_Sultana")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","supersecretkey123")


@destination_bp.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.get_all_destinations()
    return jsonify(destinations), 200


@destination_bp.route('/destinations', methods=['POST'])
def add_destination():
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
        current_user_email = decoded_token.get('sub')  # 'sub' should contain the email
        role = decoded_token.get('role')  # Retrieve the user's role

        # Check if the user has the admin role
        if role.lower() != "admin":
            return jsonify({"message": "Unauthorized access. Admin role required."}), 403

        # Retrieve the destination data from the request
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify({"message": "Invalid JSON data"}), 400

        # Validate input data
        name = data.get("name")
        description = data.get("description")
        location = data.get("location")

        if not all([name, description, location]):
            return jsonify({"message": "All fields (name, description, location) are required"}), 400

        if not isinstance(name, str) or not isinstance(description, str) or not isinstance(location, str):
            return jsonify({"message": "All fields (name, description, location) must be strings"}), 422

        # Add the destination (assuming Destination.add_destination() is a valid method)
        new_destination = Destination.add_destination(name, description, location)

        return jsonify({"message": "Destination added successfully", "destination": new_destination}), 201

    except IndexError:
        return jsonify({"message": "Bearer token malformed"}), 400
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


# Endpoint to delete a destination (Admin-only)
@destination_bp.route('/destinations/<int:id>', methods=['DELETE'])
def delete_destination(id):
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing Authorization header"}), 401

    try:
        # Extract the token and decode it
        token = auth_header.split()[1]
        decoded_token = decode_token(token)

        # Check the user's role from the token
        role = decoded_token.get("role")
        if role.lower() != "admin":
            return jsonify({"message": "Unauthorized access. Admin role required."}), 403

        # Retrieve the destination by ID
        destination = Destination.get_destination_by_id(id)
        if not destination:
            return jsonify({"message": "Destination not found."}), 404

        # Proceed with deleting the destination
        Destination.delete_destination(id)

        return jsonify({"message": "Destination deleted successfully!"}), 200

    except IndexError:
        return jsonify({"message": "Bearer token malformed"}), 400
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
