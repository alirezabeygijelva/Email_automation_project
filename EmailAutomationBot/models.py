from django.db import models
from django.contrib.auth.models import User

# مدل برای هر ایمیل 
class Email(models.Model):
    CHOICES = (
        ("gmail", "gmail"),
        ("azure", "azure"),
    )
    email_address = models.EmailField(max_length=254, primary_key=True)
    email_type = models.CharField(max_length=50, choices=CHOICES)

    def __str__(self):
        return self.email_address

# این برای این هست که آخرین تیام ثبت شده رو ثبت کنه و اون رو بخونه
class LastEmailDateTimeRead(models.Model):
    email_address = models.OneToOneField(
        Email, on_delete=models.CASCADE, primary_key=True)
    lastemailreaddatetime = models.DateTimeField()

    def __str__(self):
        schema = f"{self.email_address} - {self.lastemailreaddatetime}"
        return schema

# این مدل برای هر گروه تلگرامی هست 
class TelegramGroup(models.Model):
    group_name = models.CharField(max_length=50)
    group_url = models.URLField(max_length=260)  # url of group
    group_id = models.CharField(max_length=60, primary_key=True)

    def __str__(self):
        schema = f"{self.group_name}"
        return schema

# این مدل برای ذخیره هر ربات تلگرامی هست
class TelegramBot(models.Model):
    bot_name = models.CharField(max_length=50)
    bot_id = models.URLField(max_length=260)
    bot_token = models.CharField(max_length=50, primary_key=True)

    # def __str__(self):
    #     return self.bot_token

# این برای اطلاعات لازم برای متصل شدن به هر ایمیل هست
class MailServerAuthenticationInfo(models.Model):
    server_name = models.CharField(max_length=150, null=False, blank=False)
    password = models.CharField(max_length=350, null=True, blank=True)
    tenant_id = models.CharField(max_length=350)
    client_id = models.CharField(max_length=350)
    secret = models.CharField(max_length=350)
    authority = models.CharField(max_length=350)
    scope = models.CharField(max_length=350)

    def __str__(self):
        return str(self.id)

# این برای ریلشن ها هست
class BotGroupEmailUserRelations(models.Model):
    email_address = models.ForeignKey(Email, on_delete=models.CASCADE)
    group_id = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE)
    bot_id = models.ForeignKey(TelegramBot, on_delete=models.CASCADE)
    server_name = models.ForeignKey(
        MailServerAuthenticationInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email_address} - {self.group_id} - {self.bot_id}"

# برای فایل مدل هست و برای ذخیره فایل های پیوست
class FileModel(models.Model):
    file_data = models.FileField(unique=True)

# این مدل برای ذخیره اکتیو بات ها هست
class ActivateTelegramBots(models.Model):
    CHOICES = (
        ("active","Active"),
        ("deactive","Deactive"),
    )
    bot_token = models.CharField(max_length=250)
    status    = models.CharField(max_length=50,choices = CHOICES)

    def __str__(self):
        return self.bot_token
