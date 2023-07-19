import os
from dotenv import load_dotenv


def load_environment():
    load_dotenv()
    return {
        'REDIS_URL': os.getenv('REDIS_URL'),
        'OPENAI_API_KEY': os.getenv('apikey')
    }
