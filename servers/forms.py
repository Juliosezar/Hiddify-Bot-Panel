from django import forms
from django.core.exceptions import ValidationError
from .models import Server


class AddServerForm(forms.Form):
    ID = forms.IntegerField(required=True)
    name = forms.CharField(max_length=30, required=True)
    server_domain = forms.CharField(max_length=80, required=True)
    proxy_path = forms.CharField(max_length=60, required=True)
    admin_uuid = forms.UUIDField(required=True)
    fake_domain = forms.CharField(max_length=60, required=True)
    port = forms.IntegerField(min_value=0, required=True)
    sellers_sub_uuid = forms.UUIDField(required=True)
    bot_sub_uuid = forms.UUIDField(required=False)
    active = forms.BooleanField(required=False, initial=False)
    old_iphone = forms.BooleanField(required=False, initial=False)

    def clean_server_url(self):
        url = self.cleaned_data['server_url']
        if not url.startswith('http') or not url.endswith("/") or "panel/" in url:
            raise ValidationError("url اشتباه است.")
        return url


class EditServerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.server_id = kwargs.pop('server_id', None)
        super().__init__(*args, **kwargs)
        server = Server.objects.get(server_id=self.server_id)
        self.fields["name"].initial = server.server_name
        self.fields["proxy_path"].initial = server.server_url
        self.fields["port"].initial = server.username
        self.fields["server_domain"].initial = server.password
        self.fields["fake_domain"].initial = server.server_fake_domain
        self.fields["admin_uuid"].initial = server.inbound_id
        self.fields["sellers_sub_uuid"].initial = server.inbound_port
        self.fields["bot_sub_uuid"].initial = server.active
        self.fields["active"].initial = server.iphone
        self.fields["old_iphone"].initial = server.iphone

    name = forms.CharField(max_length=30, required=True)
    proxy_path = forms.CharField(max_length=60, required=True)
    port = forms.IntegerField(min_value=0,required=True)
    server_domain = forms.CharField(max_length=30, required=True)
    fake_domain = forms.CharField(max_length=40, required=True)
    admin_uuid = forms.UUIDField(required=True)
    sellers_sub_uuid = forms.UUIDField(required=True)
    bot_sub_uuid = forms.UUIDField(required=False)
    active = forms.BooleanField(required=False)
    old_iphone = forms.BooleanField(required=False)
    def clean_server_url(self):
        url = self.cleaned_data['server_url']
        if not url.startswith('http://') or not url.endswith("/") or "panel/" in url:
            raise ValidationError("url اشتباه است.")
        return url

