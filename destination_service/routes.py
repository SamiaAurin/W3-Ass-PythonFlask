import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
@jwt_required()
def add_destination():
    try:
        # This will decode and return the JWT claims if valid
        claims = get_jwt_identity()  
        print("JWT Claims:", claims)  # Debugging line

        # Access the claims
        role = claims.get('role')
        print("User role from token:", role)  # Debugging line

        # Your usual logic here
        if role != "Admin":
            return jsonify({"message": "Unauthorized access. Admin role required."}), 403

        # Proceed with adding destination
        data = request.get_json()
        print(f"Received data: {data}")
        name = data.get("name")
        description = data.get("description")
        location = data.get("location")

        if not isinstance(name, str) or not isinstance(description, str) or not isinstance(location, str):
            return jsonify({"msg": "All fields (name, description, location) must be strings"}), 422

        # Add the destination
        new_destination = Destination.add_destination(name, description, location)
        return jsonify(new_destination), 201

    except Exception as e:
        print(f"Error: {e}")  # Log any errors to see what's happening
        return jsonify({"message": "Unauthorized access."}), 401


# Endpoint to delete a destination (Admin-only)
@destination_bp.route('/destinations/<int:id>', methods=['DELETE'])
@jwt_required()  # Only users with a valid JWT token can access
def delete_destination(id):
    claims = get_jwt_identity()  # Extract JWT claims (e.g., email, role)
    if claims.get("role") != "admin":  # Check if the user is an admin
        return jsonify({"message": "Unauthorized access. Admin role required."}), 403
    
    destination = Destination.get_destination_by_id(id)
    if not destination:
        return jsonify({"message": "Destination not found."}), 404

    Destination.delete_destination(id)  # Delete the destination
    return jsonify({"message": "Destination deleted successfully!"}), 200
