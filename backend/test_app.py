import unittest
import requests
import subprocess
import time


class TestAppHomePage(unittest.TestCase):
    base_url = "http://127.0.0.1:8080"

    @classmethod
    def setUpClass(cls):
        # Start Flask app as a subprocess
        cls.flask_process = subprocess.Popen(
            ["python", "backend/app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        time.sleep(5)  # Allow some time for the server to start

    @classmethod
    def tearDownClass(cls):
        # Terminate the Flask app
        cls.flask_process.terminate()
        cls.flask_process.wait()

    def test_home_page(self):
        """Test the home page of the app."""
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200, "Home page should return HTTP 200")
        self.assertIn(
            "text/html", response.headers["Content-Type"], "Response should be HTML"
        )


if __name__ == "__main__":
    unittest.main()
