import datetime
import re

from flask_restful import Resource, reqparse
from flask import make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt

from app.api.V2.models import UserModel
from app.db_con import db_connection


class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='Username cannot be blank', type=str)
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank', type=str)
    parser.add_argument('role', required=True, help="Role cannot be blank", type=str)

    @jwt_required
    def post(self):
        args = UserRegistration.parser.parse_args()
        raw_password = args.get('password').strip()
        username = args.get('username').strip()
        email = args.get('email').strip()
        role = args.get('role').strip()
        user = UserModel.find_by_email(get_jwt_identity())

        if user[4] != "admin":
            return {"message": "You do not have authorization to access this feature"}, 401
        if role not in ["attendant", "admin"]:
            return {"message": "Please insert a role of 'attendant' or an 'admin' only."}, 400

        email_format = re.compile(r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)")

        if len(raw_password) < 6 or not (re.match(email_format, email)):
            return {'message': 'Please use a valid email and ensure the password exceeds 6 characters.'}, 400
        try:
            password = UserModel.generate_hash(raw_password)
            current_user_by_username = UserModel.find_by_username(username)
            current_user_by_email = UserModel.find_by_email(email)

            if current_user_by_username == None or current_user_by_email == None:
                result = UserModel.create_user(username, email, password, role)
                return make_response(jsonify({"message": "User created successfully"}), 201)
            else:
                return {'message': 'A user with that username or email already exists.'}
        except Exception as e:
            print(e)
            return {"message": "Something is amiss"}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank', type=str)

    def post(self):
        args = UserLogin.parser.parse_args()
        password = args.get('password')
        email = args.get('email').strip()

        # generate a hash for the password
        hash = UserModel.generate_hash(password)

        # check if user by the email exists
        current_user = UserModel.find_by_email(email)

        # compare user's password and the hashed password
        if UserModel.verify_hash(password, hash) and current_user != None:
            access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=5))
            return {
                'message': 'Log in successful!',
                'access_token': access_token
            }, 201
        else:
            return {
                'message': 'That user does not exist or Incorrect email or password. Try again'
            }, 400


class UserLogout(Resource):
    def __init__(self):
        self.db = db_connection()
        self.curr = self.db.cursor()

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist_token = """
                        INSERT INTO tokens (tokens) VALUES ('{}')
        """.format(jti)
        self.curr.execute(blacklist_token)
        self.db.commit()
        return {"msg": "Successfully logged out"}, 200
