import telebot
from .notification import Notification
import os
class TelegramBot:
    def __init__(self,bot_token,chat_id):
        self.absolute_path= os.path.dirname(__file__)
        self.bot          = telebot.TeleBot(bot_token)
        self.bot_token    = bot_token
        self.chat_id      = chat_id
        self.last_message = None
        self.BotMailSender = None
        
    def sendnotification(self,text_message):
        message = self.bot.send_message(self.chat_id,text_message)
        self.last_message = message.message_id 
        
    def sendattachmentnotification(self,attachment_name):
        if self.last_message is None:
            print("last_message is none")
            return
        self.absolute_path = os.path.join(self.absolute_path,attachment_name)
        print(self.absolute_path)
        self.bot.send_document(self.chat_id , document = open(self.absolute_path,'rb'), reply_to_message_id=self.last_message)
