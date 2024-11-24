from flask import Flask
from routes import auth_bp
from flask_jwt_extended import JWTManager, decode_token
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Initialize the JWT Manager with your app
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecretkey123")  # Set a secret key
jwt = JWTManager(app)

# Register the blueprint for authentication
app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
