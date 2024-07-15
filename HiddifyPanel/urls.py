from django.contrib import admin
from django.urls import path, include,re_path
from django.views.generic.base import RedirectView
from bot_connection.webhook import webhook

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path("", RedirectView.as_view(url="accounts/home/bot/", permanent=False)),
    path("accounts/", include("accounts.urls"), name="accounts"),
    path('admin/', admin.site.urls),

]
