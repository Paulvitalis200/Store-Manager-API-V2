import psycopg2
from psycopg2 import Error
from instance.config import Config, TestConfig
import os


def db_connection():
    variable = os.getenv("APP_SETTINGS")
    try:
        if variable == "production" or variable == "development":
            conn = psycopg2.connect(
                user=Config.USER,
                password=Config.PASSWORD,
                host=Config.HOST,
                port=Config.PORT,
                dbname=Config.DBNAME
            )
            return conn
        else:
            test_conn = psycopg2.connect(
                user=Config.USER,
                password=Config.PASSWORD,
                host=Config.HOST,
                port=Config.PORT,
                dbname=TestConfig.DBNAME
            )
            return test_conn
    except (Exception, psycopg2.DatabaseError) as error:
        return ('Failed to connect', error)


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
                    name text NOT NULL,
                    price integer NOT NULL,
                    quantity integer NOT NULL,
                    category text NOT NULL
                    )
                    """
    sales_table = """
                    CREATE TABLE IF NOT EXISTS sales (
                    id serial PRIMARY KEY NOT NULL,
                    description text NOT NULL,
                    items text NOT NULL
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
    queries = [products_table, sales_table, users_table]
    return queries


def destroy_tables():
    """ Delete tables"""
    conn = db_connection()
    curr = conn.cursor()

    users = """DROP TABLE IF EXISTS users CASCADE"""
    sales = """DROP TABLE IF EXISTS sales CASCADE"""
    product = """DROP TABLE IF EXISTS products CASCADE"""

    conn.commit()
