from flask_restful import Resource, reqparse
from flask import request

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
        products = self.ops.get_all_products()
        return {
            "status": "ok",
            "Message": "Success",
            "Products": products
        }, 200

    def post(self):
        data = request.get_json()
        args = Products.parser.parse_args()
        name = args.get('name').strip()  # removes whitespace
        price = args.get('price')
        quantity = args.get('quantity')
        category = args.get('category')
        payload = ['name', 'price', 'quantity', 'category']

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

    def delete(self, id):
        pass
