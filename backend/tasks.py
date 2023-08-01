from celery import Celery
import os
import smtplib
import time
import openai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
openai.api_key = os.getenv('apikey')


def make_celery(app_name=__name__):
    backend = broker = os.getenv('REDIS_URL')
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery()


@celery.task
def send_email_task(recipient, message, text: str):
    mailertogo_host = os.environ.get('MAILERTOGO_SMTP_HOST')
    mailertogo_port = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
    mailertogo_user = os.environ.get('MAILERTOGO_SMTP_USER')
    mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
    mailertogo_domain = os.environ.get('MAILERTOGO_DOMAIN', "mydomain.com")
    sender_user = 'noreply'
    sender_email = "@".join([sender_user, mailertogo_domain])
    sender_name = 'Example'

    prompt = f"Here is a completed therapy session:" \
             f"\n\n{text}\n\n " \
             f"For the above completed session, " \
             f"provide a summary of the session as well as expert level insights into what a good next step for " \
             f"the patient would be."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    message += response.choices[0].message.content

    for i in range(15):
        try:
            server = smtplib.SMTP(mailertogo_host, mailertogo_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(mailertogo_user, mailertogo_password)
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = 'Therapy Insights from MindMateGPT :)'
            msg.attach(MIMEText(message, _charset='utf-8'))
            server.sendmail(sender_email, recipient, msg.as_string())
            server.quit()
            return {"message": "Email sent successfully"}

        except Exception as e:
            print(e)
            time.sleep(15)
            continue
    return {"message": "Failed to send email"}
