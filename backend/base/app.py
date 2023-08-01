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
        mailertogo_domain = os.environ.get('MAILERTOGO_DOMAIN', "mydomain.com")
        sender_user = 'noreply'
        sender_email = "@".join([sender_user, mailertogo_domain])

        for attempt in range(3):
            try:
                server = smtplib.SMTP(mailertogo_host, mailertogo_port)
                print("logged in")
                server.ehlo()
                server.starttls()
                server.ehlo()
                print("logged in")
                server.login(mailertogo_user, mailertogo_password)
                print("logged in")
                message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)
                server.sendmail(sender_email, recipient, message)
                print("logged in")
                server.close()
                print("logged in")
                return {"message": "Email sent successfully"}

            except Exception as e:
                if attempt < 3:  # If it's not the last attempt
                    time.sleep(5)  # Wait for 10 seconds before the next attempt
                    continue
                else:
                    print("error")
