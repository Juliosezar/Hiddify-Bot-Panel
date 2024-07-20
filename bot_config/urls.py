from django.urls import path
from . import views
app_name = 'bot_config'

urlpatterns = [
    path("bot_create_config/<str:form_type>/", views.BotCreateConfigView.as_view(), name="bot_create_config"),
    path("config_page/<uuid:config_uuid>/", views.ConfigPageView.as_view(), name="config_page"),
    path("list_searched_configs/", views.ListConfigsSearched.as_view(), name="list_searched_configs"),
    path("list_configs/", views.ConfigsListView.as_view(), name="list_configs"),


    path("api_get_config_time_chices/", views.ApiGetConfigTimeChoices.as_view(), name="api_get_time_choices"),
    path("api_get_config_usage_chices/", views.ApiGetConfigUsageChoices.as_view(), name="api_get_usage_choices"),
    path("api_get_config_ip_limit_chices/", views.ApiGetConfigIPLimitChoices.as_view(), name="api_get_iplimit_choices"),
    path("api_get_axact_price/", views.ApiGetConfigPriceChoices.as_view(), name="api_get_axact_price"),

]
