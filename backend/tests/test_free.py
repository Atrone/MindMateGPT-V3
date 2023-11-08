from fastapi.testclient import TestClient
from backend.app import app
import unittest


class TestFreeApp(unittest.TestCase):

    def test_get_form_endpoint(self):
        try:
            client = TestClient(app)
            response = client.post("/api/getForm", headers={"Session": "test_session", 'taskResult': 'task'})
            assert response.json()['childhood'] == "Not provided" and response.json()['prompt'] != ""
        except Exception as e:
            assert 'int() argument must be a string' in e.args[0]

    def test_get_response_endpoint(self):
        try:
            client = TestClient(app)
            response = client.post("/api/therapistGPT", headers={"Session": "test_session", 'taskResult': 'task'},
                                   json={"message": "hi"})
            assert response.json() == "Something is wrong with our AI provider"
        except Exception as e:
            assert 'int() argument must be a string' in e.args[0]
