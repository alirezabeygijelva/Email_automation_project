from .emails import Email
from .dbRepository import repositoryDataForFinixmail, LastMailRead, CheckBotIsActive
import msal
import requests
from datetime import datetime
from .telegram_bot import TelegramBot
import os
from .telegram_bot_mail_sender import BotMailSender
import time
import datetime as settime
import time
import threading

from ..models import Email
from django.core.files import File
from EmailAutomationBot.models import FileModel
from django.conf import settings


class FinitxEmailReceiver(Email):
    def __init__(self):
        self.absolute_path = os.path.dirname(__file__)
        # value         = index in self.data
        # TENANT_ID     = 0
        # CLIENT_ID     = 1
        # SECRET        = 2
        # AUTHORITY     = 3
        # SCOPE         = 4
        # bot_token     = 5
        # group_id      = 6
        # email_address = 7

    def authenticate(self, informations):
        self.data = []
        self.data = informations
        self.start_time = settime.datetime.now()
        self.start_time = str(self.start_time)[:-6]
        self.start_time = self.start_time+"Z"

        is_bot_active = CheckBotIsActive()
        is_bot_active = is_bot_active.getdata(self.data[5])
        if is_bot_active is True:
            app = msal.ConfidentialClientApplication(
                self.data[1],  # client id !
                authority=self.data[3],  # authority !
                client_credential=self.data[2],  # secret id !
            )
            result = app.acquire_token_silent(
                self.data[4], account=None)  # scope !
            if not result:
                result = app.acquire_token_for_client(self.data[4])
            if "access_token" in result:
                self.headers = {
                    "Authorization": "Bearer " + result["access_token"],
                    "Content-Type": "application/json"
                }

                self.access_token = result["access_token"]
                # Replace with the email address you want to access
                self.user_id_response = requests.get(
                    "https://graph.microsoft.com/v1.0/users/" + self.data[7],
                    headers=self.headers
                )
                self.getemail()
            else:
                print("Failed to acquire")
        else:
            # continue
            pass
    def getemail(self):
        if self.user_id_response.ok:
            user_id = self.user_id_response.json()["id"]

            params = {
                "$select": "subject,from,receivedDateTime,bodyPreview",
                "$orderby": "receivedDateTime DESC",
                "$top": 20
            }
            response = requests.get(
                f"https://graph.microsoft.com/v1.0/users/{user_id}/mailfolders/inbox/messages",
                headers=self.headers,
                params=params
            )
            if response.ok:
                self.messages = response.json()["value"]
                self.send_notif()

    def send_notif(self):
        lastmail = LastMailRead()
        lastmail = lastmail.getdata(self.data[7])
        lastmail = str(lastmail)

        for message in self.messages:
            self.email_id = message['id']
            newer_date = datetime.strptime(
                message["receivedDateTime"], "%Y-%m-%dT%H:%M:%SZ")
            older_date = datetime.strptime(lastmail, "%Y-%m-%dT%H:%M:%SZ")
            if str(newer_date) > lastmail:  # check if its a new email or not
                # defind mail values for set a format for sending to bot
                email_subject = message["subject"]
                email_content = message["bodyPreview"]
                email_datetime_send = message["receivedDateTime"]
                email_sender_address = message["from"]["emailAddress"]["address"]
                email_sender_name = message["from"]["emailAddress"]["name"]
                message_format = f"⚠️New email from {email_sender_name}⚠️\n\n 📧email address: {email_sender_address} 📧\n\n 📅Date:{email_datetime_send}📅\n\n📨{email_content}📨"
                self.bot = TelegramBot(str(self.data[5]), self.data[6])
                time.sleep(10)
                astmessage_ID = self.bot.sendnotification(
                    message_format)  # send email content to telegram4
                self.check_attachment()

            else:
                pass
        self.set_time()
        return

    def check_attachment(self):
        try:
            url = f'https://graph.microsoft.com/v1.0/users/{self.data[7]}/messages/{self.email_id}?$expand=attachments'
            headers = {'Authorization': 'Bearer ' + self.access_token}
            response = requests.get(url, headers=self.headers)

            attachments = response.json().get('attachments')
            if attachments:
                attachment_ids = [attachment.get(
                    'id') for attachment in attachments]
                for attachment_id in attachment_ids:
                    download_url = f'https://graph.microsoft.com/v1.0/users/{self.data[7]}/messages/{self.email_id}/attachments/{attachment_id}/$value'
                    response = requests.get(download_url, headers=self.headers)

                    attachment_data = response.content

                    attachment_name = next(
                        (attachment["name"] for attachment in attachments if attachment["id"] == attachment_id), None)

                    attachment_extension = os.path.splitext(attachment_name)[1]

                    # save the attachment to a file with a unique name
                    attachment_filename = f'{attachment_id}{attachment_extension}'
                    attachment_path = os.path.join(
                        settings.MEDIA_ROOT, attachment_filename)

                    with open(attachment_path, 'wb') as f:
                        f.write(attachment_data)

                    # Create a File object from the saved file
                    with open(attachment_path, 'rb') as file:
                        django_file = File(file)

                        # Create a FileModel instance and save the file
                        file_model_instance = FileModel()
                        file_model_instance.file_data.save(
                            attachment_filename, django_file)
                        file_model_instance.save()

                    time.sleep(5)
                    self.bot.sendattachmentnotification(attachment_path)

        except Exception as e:
            print(e)
        return

    def send_notification(self):
        pass

    def set_time(self):
        last_mail_reader = LastMailRead()
        email_instance = Email.objects.get(email_address=self.data[7])
        set_now_time = last_mail_reader.setdata(Email.objects.get(
            email_address=self.data[7]), time=self.start_time)
