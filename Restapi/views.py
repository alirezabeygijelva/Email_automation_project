from rest_framework import viewsets, permissions, status
from EmailAutomationBot.models import Email, LastEmailDateTimeRead, TelegramGroup, TelegramBot, MailServerAuthenticationInfo, BotGroupEmailUserRelations
from .serializers import EmailSerializer, TelegramGroupSerializer, TelegramBotSerializer, MailServerAuthenticationInfoSerializer, BotGroupEmailUserRelationsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class AccessGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='operator').exists():
            return request.method in permissions.SAFE_METHODS

        elif request.user.groups.filter(name='moderator').exists():
            return True

        elif request.user.groups.filter(name='admin_group').exists():
            return True

        # elif request.user.groups.filter(name='no_access_group').exists():
        #     return False

        return False


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [permissions.IsAuthenticated, AccessGroupPermission]


class TelegramGroupViewSet(viewsets.ModelViewSet):
    queryset = TelegramGroup.objects.all()
    serializer_class = TelegramGroupSerializer
    permission_classes = [permissions.IsAuthenticated, AccessGroupPermission]


class TelegramBotViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, AccessGroupPermission]
    def list(self, request):
        queryset_for_bot = TelegramBot.objects.all()

        data = []
        for bot in queryset_for_bot:
            relation_exists = BotGroupEmailUserRelations.objects.filter(
                bot_id=bot.id).exists()
            active_status = "true" if relation_exists else "false"

            if relation_exists:
                group_names = TelegramGroup.objects.filter(botgroupemailuserrelations__bot_id=bot.id).values_list(
                    "group_name", flat=True
                )
            else:
                group_names = []

            data.append({
                "id": bot.id,
                "bot_name": bot.bot_name,
                "bot_id": bot.bot_id,
                "bot_token": bot.bot_token,
                "active": active_status,
                "groups": group_names,
            })

        return Response(data)

    def create(self, request):
        bot_name = request.data.get('bot_name')
        bot_id = request.data.get('bot_id')
        bot_token = request.data.get('bot_token')
        if TelegramBot.objects.filter(bot_token=bot_token).exists():
            return Response({
                "message": "Bot token is already taken. Please choose a different token."
            }, status=status.HTTP_400_BAD_REQUEST)
        errors = {}

        if not bot_name:
            errors['bot_name'] = "This field is required."
        if not bot_id:
            errors['bot_id'] = "This field is required."
        if not bot_token:
            errors['bot_token'] = "This field is required."

        if errors:
            return Response({
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST)
        bot = TelegramBot.objects.create(
            bot_name=bot_name, bot_id=bot_id, bot_token=bot_token)

        return Response({
            "message": "bot created successfully!",
            "bot_id": bot.id,
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            bot = TelegramBot.objects.get(id=pk)
            data = {
                "id": bot.id,
                "bot_name": bot.bot_name,
                "bot_id": bot.bot_id,
                "bot_token": bot.bot_token,
            }
            return Response(data)
        except TelegramBot.DoesNotExist:
            return Response({"message": "bot doent exist"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        bot_id = pk
        bot_name = request.data.get('bot_name')
        bot_token = request.data.get('bot_token')

        try:
            bot = TelegramBot.objects.get(id=bot_id)
            bot.bot_name = bot_name
            bot.bot_token = bot_token
            bot.save()

            return Response({
                "message": "bot updated"}, status.HTTP_201_CREATED)
        except TelegramBot.DoesNotExist:
            return Response({
                "message": "bot not found"
            }, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        bot_id = pk

        try:
            bot = TelegramBot.objects.get(id=bot_id)
            bot.delete()

            return Response({
                "message": "bot deleted successfully!",
            })
        except TelegramBot.DoesNotExist:
            return Response({
                "message": "bot doesnt found"
            }, status=status.HTTP_404_NOT_FOUND)


class MailServerAuthenticationInfoViewSet(viewsets.ModelViewSet):
    queryset = MailServerAuthenticationInfo.objects.all()
    serializer_class = MailServerAuthenticationInfoSerializer
    permission_classes = [permissions.IsAuthenticated, AccessGroupPermission]


class BotGroupEmailUserRelationsViewSet(viewsets.ModelViewSet):
    queryset = BotGroupEmailUserRelations.objects.all()
    serializer_class = BotGroupEmailUserRelationsSerializer
    permission_classes = [permissions.IsAuthenticated, AccessGroupPermission]



# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ModelCountSerializer

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        email_count = Email.objects.count()
        telegram_group_count = TelegramGroup.objects.count()
        all_telegram_bot_count = TelegramBot.objects.count()
        mail_server_auth_info_count = MailServerAuthenticationInfo.objects.count()
        bot_group_email_user_relations_count = BotGroupEmailUserRelations.objects.count()
        
        active_telegram_bot_count = 0
        telegram_bots = TelegramBot.objects.all()

        for bot in telegram_bots:
            if BotGroupEmailUserRelations.objects.filter(bot_id=bot).exists():
                active_telegram_bot_count += 1
        
        data = [
            {"model_name": "activebots", "count" : active_telegram_bot_count},
            {"model_name": "deactivebots", "count" : all_telegram_bot_count - active_telegram_bot_count},
            {"model_name": "Email", "count": email_count},
            {"model_name": "TelegramGroup", "count": telegram_group_count},
            {"model_name": "TelegramBot", "count": all_telegram_bot_count},
            {"model_name": "MailServerAuthenticationInfo", "count": mail_server_auth_info_count},
            {"model_name": "BotGroupEmailUserRelations", "count": bot_group_email_user_relations_count},
        ]

        serializer = ModelCountSerializer(data, many=True)
        return Response(serializer.data)
