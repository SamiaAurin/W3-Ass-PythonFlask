from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Destination

destination_bp = Blueprint('destination', __name__)

@destination_bp.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.get_all_destinations()
    return jsonify(destinations), 200

@destination_bp.route('/destinations/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_destination(id):
    current_user = get_jwt_identity()
    if current_user.get('role') != 'Admin':
        return jsonify({"message": "Unauthorized. Admin role required."}), 403
    
    if Destination.delete_destination(id):
        return jsonify({"message": f"Destination {id} deleted."}), 200
    return jsonify({"message": "Destination not found."}), 404
