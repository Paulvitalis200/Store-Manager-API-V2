from app.db_con import db_connection
import psycopg2.extras
import json
from passlib.hash import pbkdf2_sha256 as sha256


class ProductModel():

    def __init__(self):
        self.db = db_connection()
        self.curr = self.db.cursor()

    def save(self, name, price, quantity, category):
        payload = {
            'name': name,
            'price': price,
            'quantity': quantity,
            'category': category
        }
        query = """
                INSERT INTO products (name, price, quantity, category)
                 VALUES (%(name)s, %(price)s, %(quantity)s, %(category)s);
                """
        self.curr.execute(query, payload)
        self.db.commit()
        return payload

    def get_all_products(self):
        cur.execute(
            """
            SELECT id, name, price, quantity, category FROM products;
            """
        )
        data = cur.fetchall()
        result = []

        for i, items in enumerate(data):
            product_id, name, price, quantity, category = items
            stuff = {
                "product id": int(product_id),
                "name": name,
                "quantity": int(quantity),
                "price": int(price),
                "category": category
            }
            result.append(stuff)
        return result

    def get_each_product():
        pass


class UserModel:

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
