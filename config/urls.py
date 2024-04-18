from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Accounts/',include("Accounts.urls")),
    # path('bot/',include("EmailAutomationBot.urls")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),#برای گرفتن  توکن
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),# برای گرفتن اکسس توکن
    path('api/', include('Restapi.urls')),
    path('', include('swagger')),
]
