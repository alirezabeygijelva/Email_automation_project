import requests
import json
import msal
import os

from .dbRepository import repositoryDataForFinixmail
from .emails import Email
from .telegram_bot import TelegramBot


class SendEmail(Email):
    def __init__(self):
        self.absolute_path = os.path.dirname(__file__)
# باید بره دیتابیس و چک کنه که و ایدی گروه و ایدی ربات رو پیدا کنه

    def get_data(self, email, content, subject, selected_email, group_id, bot_id):
        self.requirementsdata = repositoryDataForFinixmail()  # getting data from database
        self.data = self.requirementsdata.getdata()
        self.email = email
        self.content = content
        self.subject = subject
        self.selected_mail = selected_email
        self.group = group_id
        self.bot_id = bot_id

        for _ in self.data:
            if _[7] == self.selected_mail:
                self.data = _
        self.authenticate()

    def authenticate(self):
        app = msal.ConfidentialClientApplication(
            client_id=self.data[1],  # client id
            authority=self.data[3],  # authority
            client_credential=self.data[2],  # secret id
        )
        result = app.acquire_token_silent(self.data[4], account=None)  # scope
        if not result:
            result = app.acquire_token_for_client(self.data[4])
        if "access_token" in result:
            self.access_token = result["access_token"]
            self.sendemail()

    def sendemail(self):
        url = f"https://graph.microsoft.com/v1.0/users/{self.selected_mail}/sendMail"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "message": {
                "subject": self.subject,
                "body": {
                    "contentType": "Text",
                    "content": self.content,
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": self.email
                        }
                    }
                ],
                "sender": {
                    "emailAddress": {
                        "address": self.selected_mail
                    }
                }
            },
            "saveToSentItems": "true"
        }
        # request for sending mail
        response = requests.post(url, headers=headers, data=json.dumps(body))

        self.bot = TelegramBot(self.bot_id, self.group)
        if response.ok:
            self.bot.sendnotification(
                f"✅sent successfully✅\n\nemail:{self.content}\n\n to {self.email}\n\n")
        else:
            self.bot.sendnotification(
                f"⚠️send email failed!⚠️\n\nemail:\n{self.content}\n\n to {self.email}\n\n status code: {response.status_code}")
