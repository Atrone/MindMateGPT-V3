from celery import Celery
import os
import smtplib

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
    server = smtplib.SMTP(mailertogo_host, mailertogo_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(mailertogo_user, mailertogo_password)
    server.sendmail(sender_email, recipient, message)
    server.close()