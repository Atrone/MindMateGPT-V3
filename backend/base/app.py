import json
import os
import smtplib
from typing import Dict
from fastapi import APIRouter

import time

def send_email(retries=3, delay=5):
    for i in range(retries):
        try:
            # your email sending code here...
            return
        except smtplib.SMTPServerDisconnected as e:
            if i < retries - 1:
                time.sleep(delay) # wait for a bit before trying again
                                                                                        continue
                                                                                                    else: # this was the last attempt
                                                                                                                    raise e from None # re-raise the last exception


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
        for attempt in range(5):
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=120)
                server.starttls()
                server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
                message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)
                server.sendmail(os.getenv("SENDER_EMAIL"), recipient, message)
                server.quit()

                return {"message": "Email sent successfully"}

            except Exception as e:
                if attempt < 4:  # If it's not the last attempt
                    time.sleep(10)  # Wait for 10 seconds before the next attempt
                    continue
                else:
                    return {"error": str(e)}
