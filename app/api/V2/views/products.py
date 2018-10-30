from flask_restful import Resource, reqparse
from flask import request, json, jsonify, make_response

from app.api.V2.models import ProductModel


class Products(Resource, ProductModel):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
    parser.add_argument('price', required=True, help=' Product price cannot be blank or a word', type=int)
    parser.add_argument('quantity', required=True, help='Product quantity cannot be blank or a word', type=int)
    parser.add_argument('category', required=True, help="Category must be specified", type=str)
    parser.add_argument('id', required=False, help="ID must not be specified", type=int)

    def __init__(self):
        self.operation = ProductModel()

    def get(self):
        products = self.operation.get_all_products()
        return {
            "status": "ok",
            "Message": "Success",
            "Products": products
        }, 200

    def post(self):
        args = Products.parser.parse_args()
        name = args.get('name').strip()  # removes whitespace
        price = args.get('price')
        quantity = args.get('quantity')
        category = args.get('category')

        try:
            product = self.operation.save(name, price, quantity, category)
            return {
                'message': 'Product created successfully!',
                'product': product,
                'status': 'ok'
            }, 201

        except Exception as my_exception:
            print(my_exception)
            return {'message': 'Something went wrong.'}, 500


class SingleProduct(Resource, ProductModel):
    def get(self, id):
        return ProductModel.get_each_product(self,id)

    def delete(self, id):
        return ProductModel.delete_product(self, id)

    def put(self, id):
        data = request.get_json()
        name = data['name']
        quantity = data['quantity']
        price = data['price']
        return ProductModel.update_product(self,id, name, quantity, price)
