import json
import os
import smtplib
from typing import Dict
from fastapi import APIRouter

import time


class BaseApp:
    def __init__(self, redis_client, openai):
        self.redis_client = redis_client
        self.openai = openai
        self.router = APIRouter()

    async def get_user_data(self, session_id: str) -> Dict:
        user_data_key = f"user_data_{session_id}"
        user_data = self.redis_client.get(user_data_key)
        if user_data is None:
            user_data = {session_id: {}}
        else:
            user_data = json.loads(user_data)
        return user_data

    async def send_email(self, recipient: str, message: str) -> Dict:
        for attempt in range(10):
            try:
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=120)
                server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
                message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)
                server.sendmail(os.getenv("SENDER_EMAIL"), recipient, message)
                server.quit()

                return {"message": "Email sent successfully"}

            except Exception as e:
                if attempt < 9:  # If it's not the last attempt
                    time.sleep(10)  # Wait for 10 seconds before the next attempt
                    continue
                else:
                    return {"error": str(e)}
