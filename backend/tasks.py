from celery import Celery
import os
import smtplib
import time
import openai

openai.api_key = os.getenv('apikey')


def make_celery(app_name=__name__):
    backend = broker = os.getenv('REDIS_URL')
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery()


@celery.task
def send_email_task(recipient, message, text: str):
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
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)
            server.sendmail(os.getenv("SENDER_EMAIL"), recipient, message)
            server.quit()
            return {"message": "Email sent successfully"}

        except Exception as e:
            time.sleep(15)
            continue
    return {"message": "Failed to send email"}
