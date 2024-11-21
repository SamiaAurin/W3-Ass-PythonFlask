from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import Swagger
from models import Destination


app = Flask(__name__)
swagger = Swagger(app, template_file='static/swagger.yaml')


# Register routes
from routes import destination_bp
app.register_blueprint(destination_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
