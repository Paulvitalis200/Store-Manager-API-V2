from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from app.db_con import db_connection, create_tables


def create_app(config):
    app = Flask(__name__)

    from instance.config import app_config
    app.config.from_object(app_config[config])
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

    db_connection()
    create_tables()

    from .api.V2 import my_apis
    app.register_blueprint(my_apis)

    jwt = JWTManager(app)

    return app
