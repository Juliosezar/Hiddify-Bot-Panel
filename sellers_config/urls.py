from django.urls import path
from . import views
app_name = 'sellers_config'

urlpatterns = [
    path('create_config/<int:seller_id>/', views.CreateConfigView.as_view(), name='create_config'),
    path("list_configs_searched/", views.SearchedConfigsView.as_view(), name='list_configs_searched'),
    path("configs_details/<uuid:uuid>/", views.ConfigDetailView.as_view(), name='config_details'),
    path("list_configs/<int:userid>/", views.ListConfigsView.as_view(), name='list_configs'),


    path("api_get_config_time_chices/", views.ApiGetConfigTimeChoices.as_view(), name="api_get_time_choices"),
    path("api_get_config_usage_chices/", views.ApiGetConfigUsageChoices.as_view(), name="api_get_usage_choices"),
    path("api_get_config_ip_limit_chices/", views.ApiGetConfigIPLimitChoices.as_view(), name="api_get_iplimit_choices"),
    path("api_get_axact_price/", views.ApiGetConfigPriceChoices.as_view(), name="api_get_axact_price"),
]
