from django.urls import path
from . import views
app_name = 'sellers_connection'

urlpatterns = [
    path("list_bots/", views.bots_list.as_view(), name="list_bots"),
]