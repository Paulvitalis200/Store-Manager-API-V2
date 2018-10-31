import psycopg2
from psycopg2 import Error


def db_connection():
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="manu2012",
            host="127.0.0.1",
            port="5432",
            database="store_manager_api"
        )
        return conn
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
                    name text NOT NULL UNIQUE,
                    price integer NOT NULL,
                    available_stock integer NOT NULL,
                    min_stock integer NOT NULL,
                    category text
                    )
                    """
    sales_table = """
                    CREATE TABLE IF NOT EXISTS sales (
                    id serial PRIMARY KEY,
                    attendant_name VARCHAR NOT NULL,
                    product_name VARCHAR NOT NULL,
                    quantity INTEGER,
                    price INTEGER,
                    total_price INTEGER
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
    queries = [products_table, sales_table, users_table, tokens_table]
    return queries


def destroy_tables():
    """ Delete tables"""
    conn = db_connection()
    curr = conn.cursor()

    users = """DROP TABLE IF EXISTS users CASCADE"""
    sales = """DROP TABLE IF EXISTS sales CASCADE"""
    product = """DROP TABLE IF EXISTS products CASCADE"""

    conn.commit()
