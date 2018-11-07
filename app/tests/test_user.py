import unittest
import json
import sys
import os


from app import create_app, db_con


REGISTER_URL = '/api/v2/auth/signup'
LOGIN_URL = '/api/v2/auth/login'

config = os.getenv('APP_SETTINGS')


class UserTestCase(unittest.TestCase):

    def setUp(self):
        """Setup"""
        self.app = create_app(config)
        self.client = self.app.test_client()
        self.register_user = {
            "email": "test@live.com",
            "password": "123456789",
            "username": "testuser",
            "role": "attendant"
        }
        self.register_user_empty_email = {
            "email": "",
            "password": "123456789",
            "username": "test",
            "role": "attendant"
        }
        self.register_user_invalid_email = {
            "email": "testlive.com",
            "password": "123456789",
            "username": "testuser",
            "role": "attendant"
        }
        self.login_user_empty_email = {
            "email": "",
            "password": "123456789"
        }
        self.login_user_empty_password = {
            "email": "vitalispaul48@live.com",
            "password": ""
        }
        self.register_user_empty_password = {
            "email": "test@live.com",
            "password": "",
            "username": "testuser",
            "role": "attendant"
        }
        self.register_user_short_password = {
            "email": "test@live.com",
            "password": "manu",
            "username": "test",
            "role": "attendant"
        }
        self.register_user_empty_username = {
            "email": "test@live.com",
            "password": "123456789",
            "username": "",
            "role": "attendant"
        }
        self.login_user = {
            "email": "vitalispaul48@live.com",
            "password": "manu2012"
        }

        self.register_user_empty_role = {
            "email": "test@live.com",
            "password": "123456789",
            "username": "test",
            "role": ""
        }

        self.register_user_empty_fields = {}

        db_con.create_tables()

    def login(self):
        res = self.client.post(
            '/api/v2/auth/login',
            data=json.dumps(
                dict(email="vitalispaul48@live.com", password="manu2012")
            ),
            content_type='application/json')
        return json.loads(res.get_data().decode("UTF-8"))['access_token']

    def test_register_empty_email(self):
        """TEST empty email sign up"""
        res = self.client.post(REGISTER_URL,
                               data=json.dumps(self.register_user_empty_email), headers=dict(Authorization="Bearer " + self.login()),
                               content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(resp_data['message'],
                         "Please use a valid email and ensure the password exceeds 6 characters.")
        self.assertEqual(res.status_code, 400)

    def test_register_invalid_email(self):
        """TEST invalid email"""
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_invalid_email),
                               content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)

    def test_register_empty_username(self):
        """TEST empty username in signup"""
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_username),
                               content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)

    def test_register_short_password(self):
        """TEST short sign up password"""
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_short_password),
                               content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)

    def test_empty_fields(self):
        """TEST short sign up password"""
        res = self.client.post(REGISTER_URL,
                               data=json.dumps(self.register_user_empty_fields),
                               headers=dict(Authorization="Bearer " + self.login()),
                               content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(resp_data['message'], {'username': "Username cannot be blank"})
        self.assertEqual(res.status_code, 400)

    def test_login_empty_email(self):
        """TEST empty email on login"""
        res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user_empty_email),
                                     content_type='application/json')
        resp_data = json.loads(res_login.data.decode())
        self.assertEqual(res_login.status_code, 400)

    def test_empty_role(self):
        """TEST short sign up password"""
        res = self.client.post(REGISTER_URL,
                               data=json.dumps(self.register_user_empty_role),
                               headers=dict(Authorization="Bearer " + self.login()),
                               content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(resp_data['message'], "Please insert a role of 'attendant' or an 'admin' only.")
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        db_con.destroy_tables()
