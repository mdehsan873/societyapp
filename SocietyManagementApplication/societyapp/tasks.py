from .email import email_message
from celery import Celery

app = Celery('tasks', )


@app.task
def send_verification_email(email_to, subject, body):
    print('hello')
    email_message(email_to, subject, body)
