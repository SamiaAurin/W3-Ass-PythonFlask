from flask import Blueprint, jsonify, request
import requests  # Add this import
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import decode_token
from models import Destination
from dotenv import load_dotenv  # Import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()  # This will load the values from .env into environment variables

# Create Blueprint
destination_bp = Blueprint('destinations', __name__)

# Admin Registration Code from Environment
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","supersecretkey123")
AUTH_SERVICE_URL = "http://127.0.0.1:5002"


@destination_bp.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.get_all_destinations()
    return jsonify(destinations), 200


@destination_bp.route('/destinations', methods=['POST'])
def add_destination():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing Authorization header"}), 401

    try:
        token = auth_header.split()[1]
        response = requests.post(f"{AUTH_SERVICE_URL}/api/auth/decode_token", json={"token": token})

        if response.status_code != 200:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        decoded_token = response.json()
        role = decoded_token.get('role')

        if role.lower() != "admin":
            return jsonify({"message": "Unauthorized access. Admin role required."}), 403

        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        location = data.get("location")

        if not all([name, description, location]):
            return jsonify({"message": "All fields (name, description, location) are required"}), 400

        new_destination = Destination.add_destination(name, description, location)
        return jsonify({"message": "Destination added successfully", "destination": new_destination}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@destination_bp.route('/destinations/<int:id>', methods=['PUT'])
def update_destination(id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing Authorization header"}), 401

    try:
        token = auth_header.split()[1]
        response = requests.post(f"{AUTH_SERVICE_URL}/api/auth/decode_token", json={"token": token})

        if response.status_code != 200:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        decoded_token = response.json()
        role = decoded_token.get('role')

        if role.lower() != "admin":
            return jsonify({"message": "Unauthorized access. Admin role required."}), 403

        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        location = data.get("location")

        updated_destination = Destination.update_destination(id, name, description, location)
        if not updated_destination:
            return jsonify({"message": "Destination not found"}), 404

        return jsonify({"message": "Destination updated successfully", "destination": updated_destination}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@destination_bp.route('/destinations/<int:id>', methods=['DELETE'])
def delete_destination(id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing Authorization header"}), 401

    try:
        token = auth_header.split()[1]
        response = requests.post(f"{AUTH_SERVICE_URL}/api/auth/decode_token", json={"token": token})

        if response.status_code != 200:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        decoded_token = response.json()
        role = decoded_token.get('role')

        if role.lower() != "admin":
            return jsonify({"message": "Unauthorized access. Admin role required."}), 403

        if not Destination.delete_destination(id):
            return jsonify({"message": "Destination not found"}), 404

        return jsonify({"message": "Destination deleted successfully!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500