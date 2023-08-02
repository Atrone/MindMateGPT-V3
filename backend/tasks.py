from celery import Celery
import os
import smtplib
import time
import openai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import html

openai.api_key = os.getenv('apikey')


def make_celery(app_name=__name__):
    backend = broker = os.getenv('REDIS_URL')
    broker_url_with_ssl = f"{broker}?ssl_cert_reqs=CERT_NONE"
    return Celery(app_name, backend=backend, broker=broker_url_with_ssl)


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

    for i in range(2):
        try:

            # Replace newlines with <br> for HTML
            safe_message = html.escape(message)

            # Replace newlines with <br> for HTML
            html_message = safe_message.replace('\n', '<br>')

            # Now use html_message in your HTML template
            html_code = """
            <html>
            <head>
                <style>
                    body {{ font-family: Arial; }}
                    h1 {{ color: #333; }}
                    p {{ line-height: 1.6; }}
                </style>
            </head>
            <body>
                <h1>Therapy Insights from MindMateGPT :)</h1>
                <p>{message}</p>
            </body>
            </html>
            """.format(message=html_message)

            # Set up email server
            server = smtplib.SMTP(mailertogo_host, mailertogo_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(mailertogo_user, mailertogo_password)

            # Create email
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = 'Therapy Insights from MindMateGPT :)'

            # Attach HTML content
            msg.attach(MIMEText(html_code, 'html'))

            # Send email
            server.sendmail(sender_email, recipient, msg.as_string())
            server.quit()
            return {"message": "Successful send email"}

        except Exception as e:
            print(e)
            time.sleep(15)
            continue
    return {"message": "Failed to send email"}
