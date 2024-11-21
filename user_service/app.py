from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from routes import user_bp
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'superjwtsecret')

    # Initialize JWT
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/users')

    # Swagger UI setup
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.yaml'
    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
