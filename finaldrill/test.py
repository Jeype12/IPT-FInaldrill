import unittest
from api import app
import warnings

class MyAppTest(unittest.TestCase):
    def setUp(self):
        app.config["Testing"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getemployee(self):
        response = self.app.get("/employee")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("James Cruz" in response.data.decode())

    def test_getemployee_by_id(self):
        response = self.app.get("/employee/2024003")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Warney Manlimot" in response.data.decode())

if __name__ == "__main__":
    unittest.main()
