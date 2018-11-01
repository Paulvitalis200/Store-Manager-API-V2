import unittest

from ... import create_app


class BaseTest(unittest.TestCase):
    def setUp(self):
        """Initialize app and define test variables"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_input(self):
        pass


if __name__ == '__main__':
    unittest.main()
