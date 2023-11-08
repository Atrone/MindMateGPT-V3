from fastapi.testclient import TestClient
from backend.app import app
import unittest


# Create a fixture for the test client that can be reused in multiple tests
def setUpModule():
    global client
    client = TestClient(app)


class TestFreeApp(unittest.TestCase):

    def test_get_form_endpoint(self):
        # No need for try-except here, let the test framework handle the exception
        response = client.post("/api/getForm", headers={"Session": "test_session", 'taskResult': 'summary: hi, '
                                                                                                 'insight: bruh'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('childhood', response.json())
        self.assertEqual(response.json()['childhood'], "Not provided")
        self.assertNotEqual(response.json()['prompt'], "")
        self.assertIn('summary', response.json())
        self.assertEqual(response.json()['summary'], ": hi,")

    def test_get_response_endpoint(self):
        response = client.post("/api/therapistGPT", headers={"Session": "test_session"}, json={"message": "hi"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Something is wrong with our AI provider")
