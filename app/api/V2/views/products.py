from flask_restful import Resource, reqparse
from flask import request, json, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.V2.models import ProductModel, UserModel


parser = reqparse.RequestParser()
parser.add_argument('name', required=True,
                    help='Product name cannot be blank', type=str)
parser.add_argument('price', required=True,
                    help=' Product price cannot be blank or a word', type=int)
parser.add_argument('category', required=True,
                    help="Category must be specified", type=str)
parser.add_argument('inventory', required=True,
                    help="Define available stock", type=int)
parser.add_argument('minimum_stock', required=True,
                    help="Define minimum stock", type=int)


class Products(Resource, ProductModel, UserModel):
    def __init__(self):
        self.operation = ProductModel()

    @jwt_required
    def get(self):
        products = self.operation.get_all_products()
        if not products:
            return {"message": "No products yet"}, 404
        return {
            "Message": "Successfully retrieved products",
            "Products": products
        }, 200

    @jwt_required
    def post(self):
        args = parser.parse_args()
        name = args.get('name').strip()
        price = args.get('price')
        category = args.get('category').strip()
        inventory = args.get('inventory')
        minimum_stock = args.get('minimum_stock')

        if not category or not name:
            return {"message": "Please put a product name and a category."}, 400

        try:
            user = UserModel.find_by_email(get_jwt_identity())
            if user[4] != "admin":
                return {"message": "You do not have authorization to access this feature"}, 401
            product = self.operation.get_item_if_exists(
                name, price, inventory, minimum_stock, category)
            return product
        except Exception as my_exception:
            print(my_exception)
            return {'message': 'Something went wrong.'}, 500


class SingleProduct(Resource, ProductModel, UserModel):
    def get(self, id):
        return ProductModel.get_each_product(self, id)

    @jwt_required
    def delete(self, id):
        user = UserModel.find_by_email(get_jwt_identity())
        if user[4] != "admin":
            return {"message": "You do not have authorization to access this feature"}, 401
        return ProductModel.delete_product(self, id)

    @jwt_required
    def put(self, id):
        args = parser.parse_args()
        name = args.get('name')
        price = args.get('price')
        category = args.get('category')
        inventory = args.get('inventory')
        minimum_stock = args.get('minimum_stock')

        user = UserModel.find_by_email(get_jwt_identity())
        if user[4] != "admin":
            return {"message": "You do not have authorization to access this feature"}, 401
        return ProductModel.update_product(self, id, name, price, inventory, minimum_stock, category)
