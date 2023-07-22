import json
import os
import smtplib
from typing import Dict
from fastapi import APIRouter


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
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)
            server.sendmail(os.getenv("SENDER_EMAIL"), recipient, message)
            server.quit()

            return {"message": "Email sent successfully"}

        except Exception as e:
            return {"message": f"Failed to send email: {str(e)}"}