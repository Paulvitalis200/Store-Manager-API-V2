from flask_restful import Resource, reqparse
from flask import request, json, jsonify, make_response
from flask_jwt_extended import jwt_required
from app.api.V2.models import ProductModel
from app.api.V2.views.users import admin_only
from functools import wraps


class Products(Resource, ProductModel):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
    parser.add_argument('price', required=True, help=' Product price cannot be blank or a word', type=int)
    parser.add_argument('category', required=True, help="Category must be specified", type=str)
    parser.add_argument('available_stock', required=True, help="Define available stock", type=int)
    parser.add_argument('min_stock', required=True, help="Define minimum stock", type=int)

    def __init__(self):
        self.operation = ProductModel()

    @jwt_required
    def get(self):
        products = self.operation.get_all_products()
        if not products:
            return {"message": "No products yet"}
        return {
            "Message": "Successfully retrieved products",
            "Products": products
        }, 200

    @jwt_required
    def post(self):
        args = Products.parser.parse_args()
        name = args.get('name').strip()  # removes whitespace
        price = args.get('price')
        category = args.get('category')
        available_stock = args.get('available_stock')
        min_stock = args.get('min_stock')

        try:
            product = self.operation.get_item_if_exists(name, price, available_stock, min_stock, category)
            return product
        except Exception as my_exception:
            print(my_exception)
            return {'message': 'Something went wrong.'}, 500


class SingleProduct(Resource, ProductModel):

    @jwt_required
    def get(self, id):
        return ProductModel.get_each_product(self, id)

    @jwt_required
    def delete(self, id):
        return ProductModel.delete_product(self, id)

    @jwt_required
    def put(self, id):
        data = request.get_json()
        name = data['name']
        price = data['price']
        available_stock = data['available_stock']
        category = data['category']
        min_stock = data['min_stock']
        return ProductModel.update_product(self, id, name, price, available_stock, min_stock, category)
