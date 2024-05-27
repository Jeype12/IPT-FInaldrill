import unittest
from api import app
import warnings

class MyAppTest(unittest.TestCase):
    def setUp(self):
        app.config["Testing"] = True
        self.app = app.test.client()

        warnings.simplefilter("ignore",category=DeprecationWarning)

    def test_index_page(self):
        response =  self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(),"<p>Hello, World!</p>")

    if __name__ == "__main__":
        unittest.main()