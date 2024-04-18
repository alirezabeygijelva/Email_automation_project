from rest_framework import serializers
from EmailAutomationBot.models import Email, LastEmailDateTimeRead, TelegramGroup, TelegramBot, MailServerAuthenticationInfo, BotGroupEmailUserRelations

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'


class TelegramGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramGroup
        fields = '__all__'

class TelegramBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = '__all__'

class MailServerAuthenticationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailServerAuthenticationInfo
        fields = '__all__'

class BotGroupEmailUserRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotGroupEmailUserRelations
        fields = '__all__'

# serializers.py

from rest_framework import serializers

class ModelCountSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    count = serializers.IntegerField()
