import psycopg2.extras

from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from app.db_con import db_connection, close_connection


class ProductModel():
    def __init__(self):
        self.db = db_connection()
        self.curr = self.db.cursor()

    def save(self, name, price, available_stock, min_stock, category):
        payload = {
            'name': name,
            'price': price,
            'category': category,
            'available_stock': available_stock,
            'min_stock': min_stock
        }
        query = """
                INSERT INTO products (name, price, available_stock, min_stock, category)
                 VALUES (%(name)s, %(price)s, %(available_stock)s, %(min_stock)s, %(category)s);
                """
        self.curr.execute(query, payload)
        self.db.commit()
        return payload

    def get_all_products(self):
        self.curr.execute(
            """
            SELECT id, name, price, available_stock, min_stock, category FROM products;
            """
        )
        data = self.curr.fetchall()
        result = []
        for i, items in enumerate(data):
            id, name, price, available_stock, min_stock, category = items
            stuff = {
                "product id": int(id),
                "name": name,
                "price": int(price),
                "available_stock": int(available_stock),
                "min_stock": int(min_stock),
                "category": category
            }
            result.append(stuff)
        return result

    def get_each_product(self, id):
        query = "SELECT * FROM products WHERE id = '{}';".format(id)
        self.curr.execute(query)
        product = self.curr.fetchone()
        if not product:
            return {"message": "No product with that id at the moment"}, 404
        product_format = {
            "product id": product[0],
            "name": product[1],
            "price": product[2],
            "available_stock": product[3],
            "min_stock": product[4],
            "category": product[5]
        }
        return {
            "message": "Product retrieved successfully", "product": product_format
        }, 200

    def delete_product(self, id):
        current = "SELECT * FROM products WHERE id = '{}'".format(id)
        self.curr.execute(current)
        product = self.curr.fetchone()
        if not product:
            return {"message": "Product with that ID does not exist."}, 404
        query = "DELETE FROM products WHERE id= '{}'".format(id)
        self.curr.execute(query)
        self.db.commit()
        product_format = {
            "product id": product[0],
            "name": product[1],
            "price": product[2],
            "available_stock": product[3],
            "min_stock": product[4],
            "category": product[5]
        }
        return {
            "message": "Deleted",
            "product": product_format
        }, 200

    def get_item_if_exists(self, name, price, available_stock, min_stock, category):
        query = "SELECT * FROM products WHERE name = '{}';".format(name)
        self.curr.execute(query)
        product = self.curr.fetchone()
        if product is None:
            return {
                "message": "Product created successfully",
                "product": self.save(name, price, available_stock, min_stock, category)
            }, 201
        else:
            return {"message": "Product already exists"}, 400

    def update_product(self, id, price, available_stock, min_stock, category):
        current = "SELECT * FROM products WHERE id = '{}'".format(id)
        self.curr.execute(current)
        product = self.curr.fetchone()
        if not product:
            return {'message': "The product doesn't exist"}, 404
        query = "UPDATE products SET name='{}' price='{}', available_stock='{}', min_stock='{}', category='{}' WHERE id='{}'".format(name, price, available_stock, min_stock, category, id)
        self.curr.execute(query)
        self.db.commit()
        product_format = {
            "product id": product[0],
            "name": product[1],
            "price": product[2],
            "available_stock": product[3],
            "min_stock": product[4],
            "category": product[5]
        }
        return {"message": "Product updated", "product": product_format}, 202

    def get_by_name(self, name):
        """fetch a single product by product_name"""
        self.curr.execute("SELECT * FROM products WHERE name = %s", (name,))
        product = self.curr.fetchone()
        return product

    def get_price(self, name):
        """fetch a single product by product_name"""
        self.curr.execute("SELECT * FROM products WHERE name = %s", (name,))
        product = self.curr.fetchone()
        return product[2]

    def get_min_stock(self, name):
        """fetch a single product by product_name"""
        self.curr.execute("SELECT * FROM products WHERE name = %s", (name,))
        product = self.curr.fetchone()
        return product[4]

    def get_available_quantity(self, name):
        """fetch a single product by product_name"""
        self.curr.execute("SELECT * FROM products WHERE name = %s", (name,))
        product = self.curr.fetchone()
        return product[3]


class UserModel:
    @staticmethod
    def create_admin():
        db = db_connection()
        curr = db.cursor()
        user = UserModel.find_by_email("vitalispaul48@live.com")
        if not user:
            return UserModel.create_user(username="PaulVitalis", email="vitalispaul48@live.com", password=UserModel().generate_hash("manu2012"), role="admin")

    @staticmethod
    def create_user(username, email, password, role):
        db = db_connection()
        curr = db.cursor()
        query = """
            INSERT INTO users (username, email, password, role) VALUES
            ('{}', '{}', '{}', '{}');
        """.format(username, email, password, role)
        curr.execute(query)
        db.commit()

    @staticmethod
    def find_by_email(email):
        db = db_connection()
        curr = db.cursor()
        query = "SELECT * FROM users WHERE email = '{}';".format(email)
        curr.execute(query)
        user = curr.fetchone()
        return user

    @staticmethod
    def find_by_username(username):
        db = db_connection()
        curr = db.cursor()
        query = "SELECT * FROM users WHERE username = '{}';".format(username)
        curr.execute(query)
        user = curr.fetchone()
        return user

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class SalesModel():
    def __init__(self):
        self.db = db_connection()
        self.curr = self.db.cursor()

    def save(self, attendant_name, product_name, quantity, price, total_price):
        payload = {
            'attendant_name': attendant_name,
            'price': product_name,
            'quantity': quantity,
            'price': price,
            'total_price': total_price
        }
        query = """
                INSERT INTO sales (attendant_name,product_name,quantity,price,total_price)
                 VALUES (%(attendant_name)s, %(product_name)s, %(quantity)s, %(price)s, %(total_price)s);
                """
        self.curr.execute(query, payload)
        self.db.commit()
        return payload

    def get_all_sales(self):
        self.curr.execute(
            """
            SELECT * FROM sales;
            """
        )
        sales = self.curr.fetchall()
        result = []
        for i, items in enumerate(sales):
            id, attendant_name, name, quantity, price, total_price = items
            stuff = {
                "sale id": id,
                "product_name": name,
                "quantity": int(quantity),
                "price": int(price),
                "total_price": total_price,
                "attendant_name": attendant_name
            }
            result.append(stuff)
        return result

    def get_each_sale(self, id):
        query = "SELECT * FROM sales WHERE id = '{}';".format(id)
        self.curr.execute(query)
        sale = self.curr.fetchone()
        sale_format = {
            "product id": sale[0],
            "attendant_name": sale[1],
            "product_name": sale[2],
            "quantity": sale[3],
            "price": sale[4],
            "total_price": sale[5]
        }
        if sale is None:
            return {"message": "No sale record with that id at the moment"}, 404
        else:
            return {
                "message": "Sale record retrieved successfully",
                "sale": sale_format
            }, 200

    def fetch_all_sales_attendant_name(self, attendant_name):
        """ fetch all sales """
        self.curr.execute("SELECT * FROM sales")
        sales = self.cur.fetchall()
        return sales
