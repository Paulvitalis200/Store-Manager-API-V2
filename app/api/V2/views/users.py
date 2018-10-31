from app.api.V2.models import UserModel
from flask_restful import Resource, reqparse
from flask import make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
import datetime

from functools import wraps

from app.db_con import db_connection


def admin_only(f):
    ''' Restrict access if not admin '''
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        user = UserModel().find_by_email(get_jwt_identity())
        if user[4] != "admin":
            return {'message': 'Unauthorized access, you must be an admin to access this level'}, 401
        return f(*args, **kwargs)
    return wrapper_function


class UserRegistration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='Username cannot be blank', type=str)
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank', type=str)
    parser.add_argument('role', required=True, help="Role cannot be blank", type=str)

    @jwt_required
    @admin_only
    def post(self):
        args = UserRegistration.parser.parse_args()
        password = UserModel.generate_hash(args.get('password'))
        username = args.get('username').strip()
        email = args.get('email').strip()
        role = args.get('role').strip()

        if role not in ["attendant", "admin"]:
            return {"message": "Please insert a role of 'attendant' or an 'admin' only."}
        try:
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
