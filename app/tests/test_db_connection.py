import unittest

from app import db_con


class TestDbConnection(unittest.TestCase):
    def test_db_connection(self):
        connection = db_con.db_connection()
        self.assertEqual(0, connection.closed)
