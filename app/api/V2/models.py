from app.db_con import db_connection


class ProductModel():

    def __init__(self):
        self.db = db_connection()

    def save(self, name, price, quantity):
        payload = {
            'name': name,
            'price': price,
            'quantity': quantity
        }
        query = """
                INSERT INTO products (name, price, quantity)
                 VALUES (%(name)s, %(price)s, %(quantity)s);
                """
        curr = self.db.cursor()
        curr.execute(query, payload)
        self.db.commit()
        return payload

    def get_all_products(self):
        dbconn = self.db
        cur = dbconn.cursor()
        cur.execute(
            """
            SELECT id, name, price, quantity FROM products;
            """
        )
        data = cur.fetchall()
        result = []

        for i, items in enumerate(data):
            product_id, name, price, quantity = items
            stuff = {
                "product id": int(product_id),
                "name": name,
                "quantity": int(quantity),
                "price": int(price)
            }
            result.append(stuff)
        return result

    def update_product(self):
        dbconn = self.db

    def get_each_product():
        pass
