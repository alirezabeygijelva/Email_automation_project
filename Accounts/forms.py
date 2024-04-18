from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class AdminUserCreationForm(UserCreationForm):
    # افزودن فیلد انتخاب گروه کاربری به فرم ثبت‌نام
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)

    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'نام کاربری'
        self.fields['password1'].widget.attrs['placeholder'] = 'رمز عبور'
        self.fields['password2'].widget.attrs['placeholder'] = 'تکرار رمز عبور'

    def save(self, commit=True):
        user = super().save(commit=False)
        # انتساب گروه انتخاب شده به کاربر
        group = self.cleaned_data['group']
        user.group = group
        if commit:
            user.save()
        return user

