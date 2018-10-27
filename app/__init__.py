from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager


def create_app(config):
    app = Flask(__name__)

    from instance.config import app_config
    app.config.from_object(app_config[config])
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

    jwt = JWTManager(app)

    return app
