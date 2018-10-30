from app.db_con import db_connection, close_connection
import psycopg2.extras
from passlib.hash import pbkdf2_sha256 as sha256


class ProductModel():

    def __init__(self):
        self.db = db_connection()
        self.curr = self.db.cursor()
        #self.close = close_connection(self.db)

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
        return payload

    def get_all_products(self):
        self.curr.execute(
            """
            SELECT id, name, price, quantity, category FROM products;
            """
        )
        data = self.curr.fetchall()
        result = []

        for i, items in enumerate(data):
            id, name, price, quantity, category = items
            stuff = {
                "product id": int(id),
                "name": name,
                "quantity": int(quantity),
                "price": int(price),
                "category": category
            }
            result.append(stuff)
        return result

    def get_each_product(self, id):
        query = "SELECT * FROM products WHERE id = '{}';".format(id)
        self.curr.execute(query)
        product = self.curr.fetchone()
        if product is None:
            return {"message": "No product with that id at the moment"}, 404
        return product

    def delete_product(self, id):
        product = self.get_each_product(id)
        if not product:
            return {"message": "Product not found"}, 404
        query = "DELETE FROM products WHERE id= '{}'".format(id)
        self.curr.execute(query)
        self.db.commit()
        return {"message": "Deleted", "product deleted": product}, 200

    def update_product(self, id, name, quantity, price):
        product = self.get_each_product(id)
        query = "UPDATE products SET name='{}', quantity='{}', price='{}' WHERE id='{}'".format(name, quantity, price, id)
        self.curr.execute(query)
        self.db.commit()
        if not product:
            return {'message': "product doesn't exist"},404
        return {"message": "Product updated", "product": product}, 200


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
