from django.contrib import admin
from django.urls import path, include,re_path
from django.views.generic.base import RedirectView
from bot_connection.webhook import webhook
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path("", RedirectView.as_view(url="accounts/home/bot/", permanent=False)),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('admin/', admin.site.urls),
    path("bot_finance/", include("bot_finance.urls", namespace="bot_finance")),
    path("bot_customers/", include("bot_customers.urls", namespace="bot_customers")),
    path("servers/", include("servers.urls", namespace="servers")),
    path("bot_config/", include("bot_config.urls", namespace="bot_configs")),
    path("sellers_config/", include("sellers_config.urls", namespace="sellers_configs")),
    path("sellers_finance/", include("sellers_finance.urls"), name="sellers_finance"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
