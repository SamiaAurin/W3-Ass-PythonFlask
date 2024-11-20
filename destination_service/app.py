from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# Mock data for travel destinations
destinations = [
    {"id": 1, "name": "Paris", "description": "City of Light", "location": "France"},
    {"id": 2, "name": "Tokyo", "description": "Bustling capital", "location": "Japan"},
    {"id": 3, "name": "New York", "description": "The Big Apple", "location": "USA"}
]

# Mock users (for role-based access simulation)
users = {
    "admin_token": {"role": "admin"},
    "user_token": {"role": "user"}
}

# Helper function to check role-based access
def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            user = users.get(token)
            if not user or user["role"] != role:
                return jsonify({"error": "Unauthorized access"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Route to get all destinations
@app.route('/destinations', methods=['GET'])
def get_destinations():
    return jsonify(destinations), 200

# Route to delete a destination (Admin-only)
@app.route('/destinations/<int:id>', methods=['DELETE'])
@require_role("admin")
def delete_destination(id):
    global destinations
    destination = next((dest for dest in destinations if dest["id"] == id), None)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404
    destinations = [dest for dest in destinations if dest["id"] != id]
    return jsonify({"message": "Destination deleted successfully"}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
