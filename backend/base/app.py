import json
from typing import Dict
from fastapi import APIRouter

from backend.base.entities import UserSessionData


class BaseApp:
    def __init__(self, redis_client, openai):
        self.redis_client = redis_client
        self.openai = openai
        self.router = APIRouter()

    async def get_user_data_dict(self, session_id: str) -> Dict:
        user_data_key = f"user_data_{session_id}"
        try:
            user_data = self.redis_client.get(user_data_key)
        except Exception as e:
            print(e)
            return {}
        if user_data is None:
            user_data = {}
        else:
            user_data = json.loads(user_data)
        return user_data

    async def get_user_data_dataclass(self, session_id: str) -> UserSessionData:
        user_data_dict = await self.get_user_data_dict(session_id)
        user_data = UserSessionData(**user_data_dict)
        return user_data
