from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('city',)


class RewrittenCreationForm(CustomUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].label = 'Имя'
        self.fields['city'].label = 'Из какого вы города:'
        self.fields['password1'].help_text = ''
        self.fields['password1'].label = "Придумайте пароль (не менее 8 символов)"
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = "Повторите пароль"


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
