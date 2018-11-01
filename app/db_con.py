import psycopg2
from psycopg2 import Error
import os

config_name = os.getenv('APP_SETTINGS')
dev_url = os.getenv('DEVELOPMENT_URL')
test_url = os.getenv('TESTING_URL')
production_url = os.getenv('PRODUCTION_URL')


def db_connection():
    try:
        conn = psycopg2.connect(dev_url)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        return ('Failed to connect', error)


conn = db_connection()
print(conn)


def close_connection(db_conn):
    db_conn.commit()
    db_conn.close()


def create_tables():
    conn = db_connection()
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    curr.close()
    conn.commit()


def tables():
    products_table = """
                    CREATE TABLE IF NOT EXISTS products (
                    id serial PRIMARY KEY NOT NULL,
                    name text NOT NULL UNIQUE,
                    price integer NOT NULL,
                    inventory integer NOT NULL,
                    minimum_stock integer NOT NULL,
                    category text
                    )
                    """
    sales_table = """
                    CREATE TABLE IF NOT EXISTS sales (
                    id serial PRIMARY KEY,
                    sold_by varchar NOT NULL,
                    product_name varchar NOT NULL,
                    quantity integer NOT NULL,
                    price integer NOT NULL,
                    total_price integer
                    )
                 """
    users_table = """
                    CREATE TABLE IF NOT EXISTS users (
                    id serial PRIMARY KEY NOT NULL,
                    username text UNIQUE NOT NULL,
                    email text NOT NULL,
                    password text NOT NULL,
                    role text NOT NULL
                    )
                """
    tokens_table = """
                CREATE TABLE IF NOT EXISTS tokens (
                id serial PRIMARY KEY NOT NULL,
                tokens varchar
                )
    """

    fix = """CREATE EXTENSION IF NOT EXISTS citext;"""

    alteration = """ALTER TABLE products ALTER COLUMN name TYPE citext;"""

    queries = [products_table, sales_table, users_table, tokens_table, fix, alteration]

    return queries


def destroy_tables():
    """ Delete tables"""
    conn = db_connection()
    curr = conn.cursor()
    users = """DROP TABLE IF EXISTS users CASCADE"""
    sales = """DROP TABLE IF EXISTS sales CASCADE"""
    product = """DROP TABLE IF EXISTS products CASCADE"""
    conn.commit()
