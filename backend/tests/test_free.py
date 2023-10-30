from fastapi.testclient import TestClient
from backend.app import app
from backend.base.entities import UserData
from backend.base.free.service import FreeAppService
import unittest

client = TestClient(app)


class TestFreeApp(unittest.TestCase):
    async def test_format_prompt(self):
        service = FreeAppService(initial_prompt="Test: {childhood}", openai=None)
        user_data = UserData(childhood="test_childhood")
        formatted_prompt = await service.format_prompt(user_data)
        assert formatted_prompt == "Test: test_childhood"

    def test_get_form_endpoint(self):
        try:
            response = client.post("/api/getForm", headers={"Session": "test_session", 'taskResult': 'task'})
        except Exception as e:
            assert 'int() argument must be a string' in e.args[0]
