import unittest
from api import app
import warnings
from base64 import b64encode

class MyAppTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)
        self.auth_header = {
            "Authorization": "Basic " + b64encode(b"admin1:root1").decode("utf-8")
        }

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        expected_content = (
            "<style>\n"
            "    p {\n"
            "        font-family: Times New Roman, sans-serif;\n"
            "        font-size: 100px;\n"
            "        color: white;\n"
            "        text-align: center;\n"
            "        background-color: black;\n"
            "    }\n"
            "</style>\n"
            " <p>WELCOME TO KWIKKWIK DATABASE</p>"
        )


    def test_get_employee(self):
        response = self.app.get("/employee", headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_employee_by_id(self):
        response = self.app.get("/employee/4", headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("EmployeeID", data[0])
            self.assertEqual(data[0]["EmployeeID"], 4)

if __name__ == "__main__":
    unittest.main()
