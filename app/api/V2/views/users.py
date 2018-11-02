from app.api.V2.models import UserModel
from flask_restful import Resource, reqparse
from flask import make_response, jsonify
from flask_jwt_extended import create_access_token
import datetime


class UserRegistration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='Username cannot be blank', type=str)
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank', type=str)
    parser.add_argument('role', required=True, help="Role cannot be blank", type=str)

    def post(self):
        args = UserRegistration.parser.parse_args()
        password = UserModel.generate_hash(args.get('password'))
        username = args.get('username').strip()
        email = args.get('email').strip()
        role = args.get('role')
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
