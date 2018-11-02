from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager

from app.db_con import db_connection, create_tables, destroy_tables
from app.api.V2.models import UserModel


def create_app(config):
    app = Flask(__name__)

    from instance.config import app_config
    app.config.from_object(app_config[config])

    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    db_connection()
    create_tables()
    UserModel.create_admin()

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        curr = db_connection().cursor()
        jti = decrypted_token['jti']
        curr.execute("SELECT * FROM tokens WHERE tokens = '{}'".format(jti))
        bt = curr.fetchone()
        return bt

    from .api.V2 import my_apis
    app.register_blueprint(my_apis)

    return app
