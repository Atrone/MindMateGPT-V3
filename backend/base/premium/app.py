import json
import os
import smtplib
from fastapi import Request

from backend.auth.python_auth import check_key
from backend.base.app import BaseApp
from backend.base.premium.service import create_insights
from backend.base.premium.request_models import InsightBody


class PremiumApp(BaseApp):
    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)

        @self.router.post("/download")
        async def download_insights(request: Request, body: InsightBody):
            if await check_key(body.key,self.redis_client):
                session_id = request.headers['Session']
                user_data_key = f"user_data_{session_id}"
                user_data = redis_client.get(user_data_key)
                if user_data is None:
                    user_data = {session_id: {}}
                else:
                    user_data = json.loads(user_data)

                message = user_data[session_id]['transcript'] + "\n\n\n\n" + await create_insights(self.openai,
                        user_data[session_id]['transcript'])

                try:
                    # Connect to the SMTP server
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
                    message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)

                    # Send the email
                    server.sendmail(os.getenv("SENDER_EMAIL"), body.recipient, message)
                    server.quit()

                    return {"message": "Email sent successfully"}

                except Exception as e:
                    return {"message": f"Failed to send email: {str(e)}"}
            else:
                return None