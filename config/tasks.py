from EmailAutomationBot.Email_Authomation_v1_2 import email_sender,telegram_bot,telegram_bot_mail_sender,recieve_email
from celery import Celery
# from datetime import datetime
from celery import app

@app.task
def get_emails():
    Logger.info('started!')
    a = recieve_email.FinitxEmailReceiver()
    a.authenticate()
# get_emails.delay()
