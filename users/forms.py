from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('city',)

    labels = {
        "username": "Имя",
        # "email": "Email",
        "city": "Город",
    }

    # widgets = {
    #     "text": forms.Textarea(
    #         attrs={'placeholder': 'Есть что сказать?'}),
    # }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields