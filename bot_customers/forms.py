from django import forms
from .models import Customer

class SearchUserForm(forms.Form):
    search_user = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Search Userid or Username'}))


class SendMessageToCustomerForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=True)


class ChangeWalletForm(forms.Form):
    wallet = forms.IntegerField(max_value=999,min_value=0)


class RegisterConfigToCustumerForm(forms.Form):
    user_id = forms.IntegerField(min_value=1000)

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        if not Customer.objects.filter(chat_id=user_id).exists():
            raise forms.ValidationError("User does not exist in Bot Database")
        return int(user_id)