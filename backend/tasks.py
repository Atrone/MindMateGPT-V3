from celery import Celery
import os

def make_celery(app_name=__name__):
    backend = broker = os.getenv('REDIS_URL')
    return Celery(app_name, backend=backend, broker=broker)

celery = make_celery()

@celery.task
def send_email_task(recipient, message):
    mailertogo_host = os.environ.get('MAILERTOGO_SMTP_HOST')
    mailertogo_port = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
    mailertogo_user = os.environ.get('MAILERTOGO_SMTP_USER')
    mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
    mailertogo_domain = os.environ.get('MAILERTOGO_DOMAIN', "mydomain.com")
    sender_user = 'noreply'
    sender_email = "@".join([sender_user, mailertogo_domain])

    for attempt in range(3):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            message = 'Subject: {}\n\n{}'.format("Therapy Insights from MindMateGPT Premium :)", message)
            server.sendmail(os.getenv("SENDER_EMAIL"), recipient, message)
            server.quit()
            return {"message": "Email sent successfully"}

        except Exception as e:
            print(e)
            time.sleep(10)
            continue
    return {"message": "Email not sent successfully"}
