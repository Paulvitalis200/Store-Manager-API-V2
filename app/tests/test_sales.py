import unittest
import os

from flask import json

from app import create_app

POST_PRODUCT_URL = '/api/v2/sales'
GET_SINGLE_PRODUCT = '/api/v2/products/1'
GET_ALL_PRODUCTS = '/api/v2/products'

config = os.getenv('APP_SETTINGS')


class ProductTest(unittest.TestCase):
  def setUp(self):
    """Initialize app and define test variables"""
    self.app = create_app(config)
    self.client = self.app.test_client()
    self.products = {
        "name": "Playstation 4",
        "quantity": 20
    }
    self.empty_name = {
        "name": "",
        "quantity": 20
    }

    self.empty_price = {
        "name": "Playstation 4",
        "quantity": ""
    }

  def login(self):
    res = self.client.post(
        '/api/v2/auth/login',
        data=json.dumps(
            dict(email="vitalispaul48@live.com", password="manu2012")
        ),
        content_type='application/json')
    return json.loads(res.get_data().decode("UTF-8"))['access_token']

  def login_attendant(self):
    res1 = self.client.post(
        '/api/v2/auth/signup',
        data=json.dumps(
            dict(
                username="paul200",
                email="vitalman@gmail.com",
                password="manu2012",
                role="attendant"
            )
        ), headers=dict(Authorization="Bearer " + self.login()),
        content_type='application/json')
    res = self.client.post(
        '/api/v2/auth/login',
        data=json.dumps(
            dict(email="vitalman@gmail.com", password="manu2012")
        ),
        content_type='application/json')
    return json.loads(res.get_data().decode("UTF-8"))['access_token']

  def test_empty_name(self):

    res = self.client.post(POST_PRODUCT_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_name),
                           headers=dict(
                               Authorization="Bearer " + self.login_attendant())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], "Product does not exist")
    self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
  unittest.main()
