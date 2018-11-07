import unittest
import os

from flask import json

from app import create_app

POST_SALE_URL = '/api/v2/sales'
GET_SINGLE_SALE = '/api/v2/sales/1'
GET_ALL_SALES = '/api/v2/products'

config = os.getenv('APP_SETTINGS')


class ProductTest(unittest.TestCase):
  def setUp(self):
    """Initialize app and define test variables"""
    self.app = create_app(config)
    self.client = self.app.test_client()
    self.products = {
        "name": "Playstation 5",
        "quantity": 20
    }
    self.empty_name = {
        "name": "",
        "quantity": 20
    }

    self.empty_quantity = {
        "name": "Playstation 4",
        "quantity": ""
    }

    self.products_post = {
        "name": "Playstation 4",
        "price": 40000,
        "inventory": 3000000,
        "minimum_stock": 200,
        "category": "gaming"
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

  def test_post_wrong_sale(self):
    res = self.client.post(POST_SALE_URL,
                           content_type='application/json',
                           data=json.dumps(self.products),
                           headers=dict(
                               Authorization="Bearer " + self.login_attendant())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], "Product does not exist")
    self.assertEqual(res.status_code, 404)

  def test_empty_name(self):
    res = self.client.post(POST_SALE_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_name),
                           headers=dict(
                               Authorization="Bearer " + self.login_attendant())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], "Product does not exist")
    self.assertEqual(res.status_code, 404)

  def test_empty_quantity(self):
    res = self.client.post(POST_SALE_URL,
                           content_type='application/json',
                           data=json.dumps(self.empty_quantity),
                           headers=dict(
                               Authorization="Bearer " + self.login_attendant())
                           )
    data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(data['message'], {"quantity": "Sales quantity cannot be blank or a word"})
    self.assertEqual(res.status_code, 400)

  def test_get_all_sales(self):
    """TEST whether the API can get all product(POST)"""
    res = self.client.post(POST_SALE_URL,
                           content_type='application/json',
                           headers=dict(Authorization="Bearer " + self.login_attendant()),
                           data=json.dumps(self.products))
    self.assertEqual(res.status_code, 404)
    res = self.client.get(GET_ALL_SALES,
                          headers=dict(Authorization="Bearer " + self.login()),
                          content_type='application/json')
    resp_data = json.loads(res.data.decode())
    self.assertEqual(res.status_code, 404)

  def test_get_no_single_sale(self):
    """Test API can get a single record by using it's id."""
    '''Add a product'''
    res = self.client.get(GET_SINGLE_SALE,
                          headers=dict(Authorization="Bearer " + self.login()),
                          content_type='application/json')
    resp_data = json.loads(res.get_data().decode("UTF-8"))
    self.assertEqual(res.status_code, 404)
    self.assertEqual(resp_data['message'], "No sale record with that id at the moment")
