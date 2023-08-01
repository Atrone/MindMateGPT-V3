from fastapi import Request
from backend.app import send_email_task
from backend.auth.keys import check_key
from backend.base.app import BaseApp
from backend.base.premium.service import create_insights
from backend.base.premium.request_models import InsightBody
from celery import Celery
import os

def make_celery(app_name=__name__):
    backend = broker = os.getenv('REDIS_URL')
    return Celery(app_name, backend=backend, broker=broker)

celery = make_celery()

@celery.task
def send_email_task(email_data):
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
            print(e)
            time.sleep(10)
            continue
    return {"message": "Email not sent successfully"}


class PremiumApp(BaseApp):
    def __init__(self, redis_client, openai):
        super().__init__(redis_client, openai)

        @self.router.post("/download")
        async def download_insights(request: Request, body: InsightBody):
            if await check_key(body.key, self.redis_client):
                session_id = request.headers['Session']
                user_data = await self.get_user_data(session_id)

                message = user_data[session_id]['transcript'] + "\n\n\n\n" + await create_insights(self.openai,
                                                                                                   user_data[
                                                                                                       session_id][
                                                                                                       'transcript'])

                send_email_task.delay(body.recipient, message)
                return "sent"
            else:
                return None
