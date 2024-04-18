from django.urls import path
from .views import UserRegisterView, UserEditView, UserDeleteView, UserListView
from .views import ChangePasswordView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('<int:pk>/', UserEditView.as_view(), name='user-edit'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]



