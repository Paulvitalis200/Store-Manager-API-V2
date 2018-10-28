from flask_restful import Resource, reqparse
from flask import request

from app.api.V2.models import ProductModel


class Products(Resource, ProductModel):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
    parser.add_argument('price', required=True, help=' Product price cannot be blank or a word', type=int)
    parser.add_argument('quantity', required=True, help='Product quantity cannot be blank or a word', type=int)

    def __init__(self):
        self.ops = ProductModel()

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
        payload = ['name', 'price', 'quantity']

        if not name or not price or not quantity:
            return {'message': 'Product name, price and quantity are all required'}, 400
        else:
            # Check if the item is not required
            for item in data.keys():
                if item not in payload:
                    return {"message": "The field '{}' is not required for the products".format(item)}, 400

        try:
            product = self.ops.save(name, price, quantity)
            return {
                'message': 'Product created successfully!',
                'product': product,
                'status': 'ok'
            }, 201

        except Exception as my_exception:
            print(my_exception)
            return {'message': 'Something went wrong.'}, 500

        def update(self, id):
            pass

        def delete(self, id):
