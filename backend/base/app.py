from fastapi import APIRouter


class BaseApp:
    def __init__(self, redis_client, openai):
        self.redis_client = redis_client
        self.openai = openai
        self.router = APIRouter()
