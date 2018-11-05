import unittest
import os

from flask import json

from app import create_app

POST_PRODUCT_URL = '/api/v2/products'
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
            "price": 40000,
            "inventory": 300,
            "minimum_stock": 200,
            "category": "gaming"
        }
        self.empty_name = {
            "name": "",
            "price": 40000,
            "inventory": 300,
            "minimum_stock": 200,
            "category": "gaming"
        }

        self.empty_price = {
            "name": "Playstation 4",
            "price": "",
            "inventory": 300,
            "minimum_stock": 200,
            "category": "gaming"
        }

        self.empty_inventory = {
            "name": "Playstation 4",
            "price": 40000,
            "inventory": "",
            "minimum_stock": 200,
            "category": "gaming"
        }

        self.empty_min_stock = {
            "name": "Playstation 4",
            "price": 40000,
            "inventory": 4999,
            "minimum_stock": "",
            "category": "gaming"
        }

        self.empty_category = {
            "name": "Playstation 4",
            "price": 40000,
            "inventory": 400,
            "minimum_stock": 200,
            "category": " "
        }

    def login(self):
        res = self.client.post(
            '/api/v2/auth/login',
            data=json.dumps(
                dict(email="vitalispaul48@live.com", password="manu2012")
            ),
            content_type='application/json')
        return json.loads(res.get_data().decode("UTF-8"))['access_token']

    def test_empty_products(self):
        res = self.client.post(POST_PRODUCT_URL,
                               content_type='application/json',
                               data=json.dumps(self.empty_name),
                               headers=dict(
                                   Authorization="Bearer " + self.login())
                               )
        data = json.loads(res.get_data().decode("UTF-8"))
        self.assertEqual(res.status_code, 400)

    def test_empty_category(self):
        res = self.client.post(POST_PRODUCT_URL,
                               content_type='application/json',
                               data=json.dumps(self.empty_category),
                               headers=dict(
                                   Authorization="Bearer " + self.login())
                               )
        data = json.loads(res.get_data().decode("UTF-8"))
        self.assertEqual(res.status_code, 400)

    def test_empty_min_stock(self):
        res = self.client.post(POST_PRODUCT_URL,
                               content_type='application/json',
                               data=json.dumps(self.empty_min_stock),
                               headers=dict(
                                   Authorization="Bearer " + self.login())
                               )
        data = json.loads(res.get_data().decode("UTF-8"))
        self.assertEqual(res.status_code, 400)

    def test_empty_inventory(self):
        res = self.client.post(POST_PRODUCT_URL,
                               content_type='application/json',
                               data=json.dumps(self.empty_inventory),
                               headers=dict(
                                   Authorization="Bearer " + self.login())
                               )
        data = json.loads(res.get_data().decode("UTF-8"))
        self.assertEqual(res.status_code, 400)

    def test_empty_price(self):
        res = self.client.post(POST_PRODUCT_URL,
                               content_type='application/json',
                               data=json.dumps(self.empty_price),
                               headers=dict(
                                   Authorization="Bearer " + self.login())
                               )
        data = json.loads(res.get_data().decode("UTF-8"))
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
