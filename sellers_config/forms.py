from django import forms
from sellers_finance.models import SellersPrices
from django.core.exceptions import ValidationError
from accounts.models import User

class CreateConfigForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.seller_id = kwargs.pop('seller_id', None)
        super().__init__(*args, **kwargs)
        self.fields["type"].choices = self.type_limit()

    def type_limit(self):
        types = [('limited','حجمی')]
        if SellersPrices.objects.filter(usage_limit=0, seller_id=self.seller_id).exists():
            types.append(('usage_unlimit', "حجم نامحدود"))
        if SellersPrices.objects.filter(expire_limit=0, seller_id=self.seller_id).exists():
            types.append(('time_unlimit', "زمان نامحدود"))
        return types

    type = forms.ChoiceField(required=False,)
    usage_limit = forms.CharField(required=False, widget=forms.Select(choices=[]))
    days_limit = forms.CharField(required=False, widget=forms.Select(choices=[]))
    ip_limit = forms.CharField(required=False, widget=forms.Select(choices=[]))

    def clean_usage_limit(self):
        return self.cleaned_data.get('usage_limit')

    def clean_days_limit(self):
        return self.cleaned_data.get('days_limit')

    def clean_ip_limit(self):
        return self.cleaned_data.get('ip_limit')


class ManualCreateConfigForm(forms.Form):
    type = forms.ChoiceField(required=False, choices=[('limited','حجمی'),('usage_unlimit', "حجم نامحدود"), ('time_unlimit', "زمان نامحدود")])
    usage_limit = forms.IntegerField(required=False)
    days_limit = forms.IntegerField(required=False)
    ip_limit = forms.ChoiceField(required=False, choices=[(1, '1 کاربره'), (2, '2 کاربره')])
    price = forms.IntegerField(required=False)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price is None:
            raise ValidationError('قیمت را وارد کنید.')
        elif not 0 <= price < 1500:
            raise ValidationError('قیمت باید بین 0 تا 1500 هزار تومان باشد.')
        return price

    def clean(self):
        type = self.cleaned_data.get('type')
        usage_limit = self.cleaned_data.get('usage_limit')
        days_limit = self.cleaned_data.get('days_limit')
        if type == "limited":
            if usage_limit is None:
                raise ValidationError('حجم کانفیگ را وارد کنید.')
            elif not 1 < usage_limit < 1000:
                raise ValidationError('حجم کانفیگ باید بین 1 تا 1000 گیگ باشد.')
            if days_limit is None:
                raise ValidationError('مدت زمان کانفیگ را وارد کنید.')
            elif not 0 < days_limit < 365:
                raise ValidationError('مدت زمان کانفیگ باید بین 1 روز تا 365 روز باشد.')
        elif type == 'usage_unlimit':
            if days_limit is None:
                raise ValidationError('مدت زمان کانفیگ را وارد کنید.')
            elif not 0 < days_limit < 365:
                raise ValidationError('مدت زمان کانفیگ باید بین 1 روز تا 365 روز باشد.')
        elif type == 'time_unlimit':
            if usage_limit is None:
                raise ValidationError('حجم کانفیگ را وارد کنید.')
            elif not 1 < usage_limit < 1000:
                raise ValidationError('حجم کانفیگ باید بین 1 تا 1000 گیگ باشد.')