from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    group = serializers.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(UserRegisterSerializer, self).__init__(*args, **kwargs)
        self.fields['group'].choices = self.get_group_choices()

    def get_group_choices(self):
        groups = Group.objects.all()
        return [(group.name, group.name) for group in groups]

    def create(self, validated_data):
        # ایجاد نمونه‌ی کاربر با استفاده از داده‌های ورودی
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # گرفتن نام گروه انتخابی از داده‌های ورودی
        group_name = validated_data['group']

        try:
            # یافتن گروه مورد نظر با نام ارسالی
            group = Group.objects.get(name=group_name)
            # اضافه کردن کاربر به گروه
            group.user_set.add(user)
        except Group.DoesNotExist:
            # اگر گروه با نام مورد نظر وجود نداشته باشد، یک خطا برمی‌گردانیم
            raise serializers.ValidationError(f"گروه '{group_name}' وجود ندارد.")

        return user

User = get_user_model()

from rest_framework import serializers
from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password', 'group']

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#         )
#         group_name = validated_data.get('group')
#         if group_name:
#             try:
#                 group = Group.objects.get(name=group_name)
#                 user.groups.add(group)
#             except Group.DoesNotExist:
#                 raise serializers.ValidationError(f"group '{group_name}' doesn't exist.")
#         return user



from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    groups_write = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field='name',
        required=False,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'groups_write']

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups_write', None)
        if groups_data is not None:
            instance.groups.clear()  # حذف تمامی گروه‌های کاربر
            for group_name in groups_data:
                group, _ = Group.objects.get_or_create(name=group_name)
                instance.groups.add(group)  # اضافه کردن گروه‌های جدید به کاربر
        for key, value in validated_data.items():
            setattr(instance, key, value)  # به‌روز رسانی سایر فیلدها
        instance.save()
        return instance






class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)
