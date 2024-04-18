from django.contrib import admin
from .models import Email, TelegramGroup, TelegramBot, BotGroupEmailUserRelations, MailServerAuthenticationInfo, FileModel, LastEmailDateTimeRead, ActivateTelegramBots
# Register your models here.
admin.site.register(Email)
admin.site.register(TelegramGroup)
admin.site.register(TelegramBot)
admin.site.register(MailServerAuthenticationInfo)
admin.site.register(BotGroupEmailUserRelations)
admin.site.register(ActivateTelegramBots)
admin.site.register(LastEmailDateTimeRead)
