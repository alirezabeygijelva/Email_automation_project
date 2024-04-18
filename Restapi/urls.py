from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailViewSet, TelegramGroupViewSet, TelegramBotViewSet, MailServerAuthenticationInfoViewSet, BotGroupEmailUserRelationsViewSet, DashboardView

router = DefaultRouter()
router.register(r'emails', EmailViewSet)
router.register(r'telegram-groups', TelegramGroupViewSet)
router.register(r'telegram-bots', TelegramBotViewSet, basename='telegrambot')
router.register(r'mail-auth-info', MailServerAuthenticationInfoViewSet)
router.register(r'config', BotGroupEmailUserRelationsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

