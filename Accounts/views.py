from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from .serializers import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from drf_yasg.utils import swagger_auto_schema

class IsInAdminGroup(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='admin_group').exists():
            return True


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            True




class UserRegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user with specified information.",
        request_body=UserRegisterSerializer,
        responses={201: "Created", 400: "Bad Request"},
    )
    def post(self, request):
        """
        Register a new user with specified information.
        """
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            user = User.objects.create_user(
                username=ser_data.validated_data['username'],
                email=ser_data.validated_data['email'],
                password=ser_data.validated_data['password'],
            )

            group_name = ser_data.validated_data['group']
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(
                    f"group '{group_name}' doesn't exist.")

            return Response(ser_data.data, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserRegisterView(APIView):
#     permission_classes = [IsAuthenticated, IsInAdminGroup]

#     def post(self, request):
#         ser_data = UserRegisterSerializer(data=request.POST)
#         if ser_data.is_valid():
#             user = User.objects.create_user(
#                 username=ser_data.validated_data['username'],
#                 email=ser_data.validated_data['email'],
#                 password=ser_data.validated_data['password'],
#             )

#             group_name = ser_data.validated_data['group']
#             try:
#                 group = Group.objects.get(name=group_name)
#                 user.groups.add(group)
#             except Group.DoesNotExist:
#                 raise serializers.ValidationError(
#                     f"group '{group_name}' doesn't exist.")

#             return Response(ser_data.data, status=status.HTTP_201_CREATED)

#         return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEditView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsInAdminGroup]

    def get_queryset(self):
        return User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # اگر نمونه‌ای از مدل ویرایش شده ارسال نشده باشد، فقط مقادیر قبلی را برگردان
        if not request.data:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)



class UserDeleteView(DestroyAPIView):
    #برای حذف یوزر 
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsInAdminGroup]

    def get_queryset(self):
        return User.objects.all()


class UserListView(ListAPIView):
    # برای نشان دادن لیست ممبر ها 
    permission_classes = [IsAuthenticated, IsInAdminGroup]
    queryset = User.objects.all()
    serializer_class = UserSerializer



# class ChangePasswordView(APIView):
#     """
#     توی این کلاس با توجه به این که کاربر احزار هویت شده است فقط نیاز است که رمز رو بنویسه تا رمزش نوشته بشه
#     و نیازی به نوشتن رمز قبلی نیست که میدانیم کیست او!
#     """
#     permission_classes = [IsAuthenticated, IsOwner]

#     def put(self, request):
#         serializer = ChangePasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # بازیابی کاربر فعلی
#         user = request.user

#         # بررسی مطابقت دو رمز عبور جدید
#         new_password = serializer.validated_data['new_password']
#         confirm_password = serializer.validated_data['confirm_password']
#         if new_password != confirm_password:
#             return Response({"message": "passwords must be the same!"}, status=status.HTTP_400_BAD_REQUEST)

#         # تغییر رمز عبور و ذخیره کاربر
#         user.set_password(new_password)
#         user.save()

#         return Response({"message": "password changed successfully!"}, status=status.HTTP_200_OK)



class ChangePasswordView(APIView):
    @swagger_auto_schema(
        operation_description="Change the password for the authenticated user.",
        request_body=ChangePasswordSerializer,
        responses={200: "OK", 400: "Bad Request"},
    )
    def put(self, request):
        """
        Change the password for the authenticated user.
        """
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the current user
        user = request.user

        # Check the consistency of the new passwords
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']
        if new_password != confirm_password:
            return Response({"message": "Passwords must be the same!"}, status=status.HTTP_400_BAD_REQUEST)

        # Change the password and save the user
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)
