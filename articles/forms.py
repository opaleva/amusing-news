from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'mail', 'text')

        labels = {
            "name": "Имя",
            "mail": "Email",
            "text": "",
        }

        widgets = {
            "text": forms.Textarea(
                attrs={'placeholder': 'Есть что сказать?'}),
        }
