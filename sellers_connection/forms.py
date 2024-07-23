from django import forms
from .models import Bots

class NewBotForm(forms.ModelForm):
    class Meta:
        model = Bots
        fields = ["name", 'bot_token', 'bot_usernamr']
