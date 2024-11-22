from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, exceptions
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from routes import destination_bp
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Debugging: Print the environment variable to confirm it's loaded
    ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE")
    
    
    # Set JWT_SECRET_KEY from .env
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey123")



    # Initialize JWT
    jwt = JWTManager(app)

    # Enable CORS for specific origin (localhost:5001)
    CORS(app)

    # Error handlers for JWT-related issues
    @app.errorhandler(exceptions.NoAuthorizationError)
    def handle_no_auth_error(e):
        return jsonify({"msg": "Authorization header is missing."}), 401


    # Register Blueprints
    app.register_blueprint(destination_bp, url_prefix='/api')

    # Swagger UI setup
    SWAGGER_URL = '/docs'  # Swagger UI endpoint
    API_URL = '/static/swagger.yaml'  # Path to the swagger.yaml file
    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5002, debug=True)
