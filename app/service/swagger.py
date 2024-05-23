from flask import current_app
from flasgger import Swagger
from ..config.swagger import swagger_config


def setup_swagger():
    """setup swagger document"""
    current_app.config['SWAGGER'] = swagger_config
    swagger = Swagger(current_app)
