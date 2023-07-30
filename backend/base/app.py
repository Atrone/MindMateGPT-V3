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
        mailertogo_host = os.environ.get('MAILERTOGO_SMTP_HOST')
        mailertogo_port = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
        mailertogo_user = os.environ.get('MAILERTOGO_SMTP_USER')
        mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')

        for attempt in range(10):
            try:
                server = smtplib.SMTP(mailertogo_host, mailertogo_port)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(mailertogo_user, mailertogo_password)
                message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)
                server.sendmail(mailertogo_user, recipient, message)
                server.quit()

                return {"message": "Email sent successfully"}

            except Exception as e:
                if attempt < 9:  # If it's not the last attempt
                    time.sleep(10)  # Wait for 10 seconds before the next attempt
                    continue
                else:
                    return {"error": str(e)}
