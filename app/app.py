from os import getenv, environ
from flask import Flask, request, jsonify
from .api import mount_routes
from .config.swagger import swagger_config
from .error import set_error_handler
from .service.swagger import setup_swagger

app = Flask(__name__)

# Load environment variables from a .env file if present
from dotenv import load_dotenv
load_dotenv()

with app.app_context():
    setup_swagger()
    mount_routes()
    set_error_handler()

if __name__ == "__main__":
    app.run("0.0.0.0", getenv("PORT", 5000))
