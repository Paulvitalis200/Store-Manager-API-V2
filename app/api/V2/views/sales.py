from flask_restful import Resource, reqparse
from flask import request, json, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.V2.models import SalesModel, ProductModel, UserModel
from app.api.V2.views.users import admin_only
from app.db_con import db_connection, close_connection


class Sales(Resource, SalesModel):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='Sales record name cannot be blank', type=str)
    parser.add_argument('quantity', required=True, help='Sales quantity cannot be blank or a word', type=int)

    def __init__(self):
        self.operation = SalesModel()
        self.conn = db_connection()
        self.curr = self.conn.cursor()

    @jwt_required
    def get(self):
        sales = self.operation.get_all_sales()
        if not sales:
            return {"message": "No sales records yet"}
        return {
            "message": "Successfully retrieved the sales records",
            "Products": sales
        }, 200

    @jwt_required
    def post(self):
        args = Sales.parser.parse_args()
        name = args.get('name').strip()  # removes whitespace
        quantity = args.get('quantity')
        attendant_name = UserModel().find_by_email(get_jwt_identity())[1]
        product = ProductModel().get_by_name(name)

        if not product:
            return {"message": "Product does not exist"}, 404

        price = ProductModel().get_price(name)
        min_stock = ProductModel().get_min_stock(name)
        available_quantity = ProductModel().get_available_quantity(name)

        if available_quantity <= min_stock:
            return {"message": "Cannot sell"}
        if quantity > available_quantity:
            return {"message": "The product is out of stock"}

        updated_quantity = available_quantity - quantity

        self.curr.execute(
            """ UPDATE products SET available_stock= %s WHERE name =%s""", (updated_quantity, name))
        self.conn.commit()

        try:
            total_price = price * quantity
            """Add a sale to the created table products """
            sale_query = "INSERT INTO sales(attendant_name,product_name,quantity,price,total_price) VALUES( %s, %s, %s, %s, %s)"
            sale_payload = (attendant_name, name, quantity, price, total_price)
            self.curr.execute(sale_query, sale_payload)
            self.conn.commit()
            return {'message': 'Sale successful', "remaining quantity": updated_quantity}, 201

        except Exception as my_exception:
            print(my_exception)
            return {'message': 'Something went wrong.'}, 500


class SingleSaleAdmin(Resource, SalesModel):

    @jwt_required
    def get(self, id):
        return SalesModel().get_each_sale(id)
