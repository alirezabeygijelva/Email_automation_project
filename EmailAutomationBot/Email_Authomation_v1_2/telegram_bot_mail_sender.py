import telebot
from telebot import types
from .email_sender import SendEmail
from .dbRepository import  GetGroupList, GetMailsList, CheckBotIsActive
from ..models import BotGroupEmailUserRelations
from .telegram_bot import TelegramBot

# # گرفتن لیست ایمیل های متصل به ربات
# def get_mails_list(bot_token, group_id):
#     result_queryset = BotGroupEmailUserRelations.objects.filter(
#         bot_id=bot_token, group_id=group_id).values('email_address')
#     _list = []
#     for _ in result_queryset:
#         _list.append(_["email_address"])
#     return _list

# # گرفتن گروه های متصل به ربات
# def get_groups_list(bot_token):
#     result_queryset = BotGroupEmailUserRelations.objects.filter(
#         bot_id=bot_token).values('group_id')
    
#     _list = []
#     for _ in result_queryset:
#         _list.append(int(_['group_id']))
#     return _list



class BotMailSender:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.chat_id = []
        self.bot = telebot.TeleBot(self.bot_token)
        self.WAITING_FOR_EMAIL = False
        self.WAITING_FOR_SUBJECT = False
        self.WAITING_FOR_CONTENT = False
        self.email_address = ""
        self.email_subject = ""
        self.email_content = ""
        self.mail_list = []
        bot_commands = [
            telebot.types.BotCommand("sendemail", "send email with telegram")
        ]
        self.bot.set_my_commands(bot_commands)

        @self.bot.message_handler(commands=['sendemail'])
        def ask_wich_email_for_send_email(message):
            bot_is_active = CheckBotIsActive()
            bot_is_active = bot_is_active.getdata(bot_token=self.bot_token)

            if bot_is_active is True:
                # self.chat_id = get_groups_list(self.bot_token)
                self.chat_id = GetGroupList()
                self.chat_id = self.chat_id.getdata(self.bot_token)
                if message.chat.id in self.chat_id:
                    self.current_chat_id = message.chat.id
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    # self.mail_list = get_mails_list(
                    #     self.bot_token, message.chat.id)
                    self.mail_list = GetMailsList()
                    self.mail_list = self.mail_list.getdata(self.bot_token, message.chat.id)
                    for mail in self.mail_list:

                        email_button = types.InlineKeyboardButton(
                            mail, callback_data=mail)
                        markup.add(email_button)
                    self.bot.send_message(
                        message.chat.id, "Choose your email", reply_markup=markup)
                else:
                    self.bot.reply_to(message, "You can't use this bot!")
            else:
                # print("not today not today")
                pass
        @self.bot.callback_query_handler(func=lambda call: call.data in self.mail_list)
        def callback_query(call):
            self.selected_email = call.data
            self.bot.answer_callback_query(
                call.id, f'{self.selected_email} selected!', show_alert=True)

            self.bot.send_message(call.message.chat.id,
                                  "Please enter the email address:")
            self.WAITING_FOR_EMAIL = True

        @self.bot.message_handler(func=lambda message: self.WAITING_FOR_EMAIL)
        def get_email_address(message):
            self.email_address = message.text
            self.WAITING_FOR_EMAIL = False

            self.bot.send_message(
                message.chat.id, "Please enter the email subject:")
            self.WAITING_FOR_SUBJECT = True

        @self.bot.message_handler(func=lambda message: self.WAITING_FOR_SUBJECT)
        def get_email_subject(message):
            self.email_subject = message.text
            self.WAITING_FOR_SUBJECT = False

            self.bot.send_message(
                message.chat.id, "Please enter the email content:")
            self.WAITING_FOR_CONTENT = True

        @self.bot.message_handler(func=lambda message: self.WAITING_FOR_CONTENT)
        def get_email_content(message):
            self.email_content = message.text
            self.WAITING_FOR_CONTENT = False
            sendemail = SendEmail()
            status_of_send = sendemail.get_data(
                self.email_address, self.email_content, self.email_subject, self.selected_email, self.current_chat_id, self.bot_token)
