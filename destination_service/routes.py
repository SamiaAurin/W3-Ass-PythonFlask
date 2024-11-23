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
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Missing Authorization header"}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = decode_token(token)
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
        decoded_token = decode_token(token)
        role = decoded_token.get("role")

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
        decoded_token = decode_token(token)
        role = decoded_token.get("role")

        if role.lower() != "admin":
            return jsonify({"message": "Unauthorized access. Admin role required."}), 403

        if not Destination.delete_destination(id):
            return jsonify({"message": "Destination not found"}), 404

        return jsonify({"message": "Destination deleted successfully!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

