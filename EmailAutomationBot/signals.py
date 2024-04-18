from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from EmailAutomationBot.models import ActivateTelegramBots, BotGroupEmailUserRelations, LastEmailDateTimeRead, Email
import telebot
from threading import Thread
from EmailAutomationBot.Email_Authomation_v1_2.telegram_bot_mail_sender import BotMailSender
import datetime

#این تابع ترد برای هر پولینگ درست میکنه
def bot_polling_thread_maker(bot_token):
    bot = BotMailSender(bot_token=bot_token)
    bot.bot.polling(non_stop=True, long_polling_timeout=10)
    
# این تابع برای استاپ کردن ربات استفاده میشه
def bot_stop_polling_thread_maker(bot_token):
    bot = BotMailSender(bot_token=bot_token)
    # bot.bot.stop_polling()
    bot.bot.stop_bot()


#این برای استارت زدن ربات وقتی که شئ جدید اضافه شد
@receiver(post_save, sender=BotGroupEmailUserRelations)
def add_bot_to_active_bots(sender, instance, **kwargs):
    
    bot_token = instance.bot_id.bot_token
    try:
        bot = ActivateTelegramBots.objects.get(bot_token=bot_token)
    except ActivateTelegramBots.DoesNotExist:
        bot = ActivateTelegramBots(bot_token=bot_token, status='active')
        bot.save()
    thread_ = Thread(target=bot_polling_thread_maker, args=(bot_token,))
    thread_.start()

# این برای حذف از دیتابیس اکتیو بات هست وقتی که یک شئ حذف شد از تیبل ریلشن ها
@receiver(post_delete, sender=BotGroupEmailUserRelations)
def remove_bot_from_active_bots(sender, instance, **kwargs):
    # bot_token = instance.bot_id.bot_token
    # try:
        
    #     bot = ActivateTelegramBots.objects.get(bot_token=bot_token)
    #     bot.delete()
    # except ActivateTelegramBots.DoesNotExist:
    #     pass
    # _bot = Thread(target=bot_stop_polling_thread_maker,args=bot_token)
    # _bot.start()
    # bot_stop_polling_thread_maker(bot_token=bot_token)
    # print("bot stoped")
    pass



@receiver(post_save,sender=Email)
def set_time_for_new_email_address(sender, instance, **kwargs):
    current_time = datetime.datetime.now()
    current_time = str(current_time)
    current_time = current_time[:-7]
    current_time = current_time+"Z"
    
    new_mail = LastEmailDateTimeRead(email_address=instance,lastemailreaddatetime=current_time)
    new_mail.save()