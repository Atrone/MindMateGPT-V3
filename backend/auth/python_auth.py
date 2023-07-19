import random
import string

from pydantic import BaseModel


class HTTPKeyCheckBody(BaseModel):
    key: str


def generate_key(length):
    # Generate a random alphanumeric key
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


async def check_key(key: str, redis_client):
    if not key or not redis_client.exists(key):
        return {"status": "failure", "message": "Invalid key."}
    return {"status": "success", "message": "Valid key."}
