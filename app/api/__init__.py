
from flask import Flask, current_app
from .common import common_api


def mount_routes():
    """
    mount routes to flask instance
    """
    current_app.register_blueprint(common_api, url_prefix="/")
    return current_app
