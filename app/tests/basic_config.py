# Standard library imports
import unittest
import json

# Local application imports
from app import create_app
from app.db_con import create_tables, destroy_tables


config_name = "testing"
app = create_app(config_name)

LOGIN_URL = "/api/v2/auth/login"
SIGN_UP_URL = "/api/v2/auth/signup"


class Settings(unittest.TestCase):
    """
    Settings class to hold all the similar test config
    """

    new_attendant = {
        "username": "Wendy200",
        "email": "marywendy@gmail.com",
        "password": "wendy2000",
        "role": "attendant"
    }
    login_data = {
        "email": "marywendy@gmail.com",
        "password": "wendy2000",
    }

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        create_tables()

    def verify_user(self):
        self.app.post(SIGN_UP_URL,
                      data=json.dumps(self.new_attendant),
                      content_type='application/json')
        return self.app.post(LOGIN_URL,
                             data=json.dumps(self.login_data),
                             content_type='application/json')

    def tearDown(self):
        destroy_tables()
