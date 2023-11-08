from fastapi.testclient import TestClient
from backend.app import app
from backend.base.entities import UserSessionData
from backend.base.free.service import FreeAppService, extract_form_data
import unittest

client = TestClient(app)


class TestFreeApp(unittest.TestCase):
    async def test_extract_form(self):
        user_data = {"childhood": "yo", "bruh": "bruh"}
        user_data = await extract_form_data(user_data)
        assert user_data == {"childhood": "bro"}

    async def test_format_prompt(self):
        service = FreeAppService(initial_prompt="Test: {childhood}", openai=None)
        user_data = UserSessionData(childhood="test_childhood")
        formatted_prompt = await service.format_prompt(user_data)
        assert formatted_prompt == "Test: test_childhood"

    def test_get_form_endpoint(self):
        try:
            response = client.post("/api/getForm", headers={"Session": "test_session", 'taskResult': 'task'})
        except Exception as e:
            assert 'int() argument must be a string' in e.args[0]

