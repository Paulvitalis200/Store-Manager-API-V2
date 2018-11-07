import unittest
import os

from flask import json

from app import create_app, db_con

POST_PRODUCT_URL = '/api/v2/products'
GET_SINGLE_PRODUCT = '/api/v2/products/1'
GET_ALL_PRODUCTS = '/api/v2/products'
USERLOGIN = '/api/v2/auth/login'

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
        "name": "  ",
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

    db_con.create_tables()

  def login(self):
    res = self.client.post(
        '/api/v2/auth/login',
        data=json.dumps(
            dict(email="vitalispaul48@live.com", password="manu2012")
        ),
        content_type='application/json')
    return json.loads(res.get_data().decode("UTF-8"))['access_token']

  def test_empty_name(self):
    res = self.client.post(POST_PRODUCT_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_name),
                           headers=dict(
                               Authorization="Bearer " + self.login())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], "Please put a product name and a category.")
    self.assertEqual(res.status_code, 400)

  def test_empty_min_stock(self):
    res = self.client.post(POST_PRODUCT_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_min_stock),
                           headers=dict(
                               Authorization="Bearer " + self.login())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], {'minimum_stock': 'Define minimum stock'})
    self.assertEqual(res.status_code, 400)

  def test_empty_inventory(self):
    res = self.client.post(POST_PRODUCT_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_inventory),
                           headers=dict(
                               Authorization="Bearer " + self.login())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], {'inventory': 'Define available stock'})
    self.assertEqual(res.status_code, 400)

  def test_empty_price(self):
    res = self.client.post(POST_PRODUCT_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_price),
                           headers=dict(
                               Authorization="Bearer " + self.login())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], {'price': ' Product price cannot be blank or a word'})
    self.assertEqual(res.status_code, 400)

  def test_empty_category(self):
    res = self.client.post(POST_PRODUCT_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_category),
                           headers=dict(
                               Authorization="Bearer " + self.login())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], "Please put a product name and a category.")
    self.assertEqual(res.status_code, 400)

  def test_get_null_products(self):
    """TEST whether the API can get all product(POST)"""
    res = self.client.get(GET_ALL_PRODUCTS,
                          headers=dict(Authorization="Bearer " + self.login()),
                          content_type='application/json')
    resp_data = json.loads(res.data.decode())
    self.assertEqual(res.status_code, 404)

  def test_get_no_product(self):
    """Test API can get a single record by using it's id."""
    '''Add a product'''
    res = self.client.get(GET_SINGLE_PRODUCT,
                          headers=dict(Authorization="Bearer " + self.login()),
                          content_type='application/json')
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(res.status_code, 404)

  def tearDown(self):
    db_con.destroy_tables()
