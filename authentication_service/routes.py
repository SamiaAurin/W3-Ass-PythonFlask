from flask import Blueprint, request, jsonify
from flask_jwt_extended import decode_token
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Load the admin registration code from environment variables
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE", "Syeda_Samia_Sultana")

auth_bp = Blueprint('auth', __name__)

# Endpoint: Validate Admin Code for Registration
@auth_bp.route('/validate_admin_code', methods=['POST'])
def validate_admin_code():
    data = request.get_json()
    admin_code = data.get('admin_code')

    if not admin_code:
        return jsonify({'error': 'Admin code is required'}), 400

    if admin_code == ADMIN_REGISTRATION_CODE:
        return jsonify({'message': 'Admin code valid, proceed with registration'}), 200
    else:
        return jsonify({'error': 'Invalid admin code'}), 403


@auth_bp.route('/decode_token', methods=['POST'])
def decode_token_endpoint():
    try:
        # Get the JWT token from the request body
        token = request.json.get('token')
        if not token:
            raise BadRequest("Token is required.")

        # Decode the token using the JWT extended decode_token function
        decoded_token = decode_token(token)
        print(decoded_token)
        # Return the decoded token details (such as email, role, etc.)
        return jsonify({
            "email": decoded_token.get('sub'),
            "role": decoded_token.get('role'),
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400
