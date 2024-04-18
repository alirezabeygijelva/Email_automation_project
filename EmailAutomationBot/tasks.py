from config.celery import app
from EmailAutomationBot.Email_Authomation_v1_2 import recieve_email, dbRepository, main
from EmailAutomationBot.Email_Authomation_v1_2.telegram_bot_mail_sender import BotMailSender
from EmailAutomationBot.Email_Authomation_v1_2.dbRepository import LastMailRead
from EmailAutomationBot.models import Email, ActivateTelegramBots, TelegramBot, BotGroupEmailUserRelations
import threading
import telebot

# تابع برای درست کردن ترد برای پولینگ
def bot_polling_thread_maker(bot_token):
    bot = BotMailSender(bot_token=bot_token)
    bot.bot.polling(non_stop=True, long_polling_timeout=10)
    # bot.bot.polling()

# ترد برای درست کردن ایمیل های جدید برای هر ایمیل جدید
def email_receiver_thread_maker(informations):
    email_receiver = recieve_email.FinitxEmailReceiver()
    email_receiver = email_receiver.authenticate(informations)

# تسک گرفتن ایمیل ها که هر 5 دقیقه یک بار صدا زده میشه و بعد از 7 دقیقه تایم لیمیت میگیره و کیل میشه
@app.task(time_limi=420)
def get_emails():
    all_data = dbRepository.repositoryDataForFinixmail()
    all_data = all_data.getdata()

    for data in all_data:
        email_receiver_thread = threading.Thread(
            target=email_receiver_thread_maker, args=(data,))
        email_receiver_thread.start()


get_emails.delay()

# این تسک برای پولینگ کردن هر تسک هست
@app.task()
def polling_bot():
    all_data = dbRepository.repositoryDataForFinixmail()
    all_data = all_data.getdata()
    data_list = []
    for data in all_data:
        inner_list = []
        if [str(data[5])] not in data_list:
            inner_list.append(str(data[5]))
            data_list.append(inner_list)
    for _ in data_list:
        _thread = threading.Thread(
            target=bot_polling_thread_maker, args=(_[0],))
        _thread.start()


polling_bot.delay()
