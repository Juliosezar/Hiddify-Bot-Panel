from django.urls import path
from . import views
app_name = 'sellers_finance'

urlpatterns = [
    path('show_prices/<int:seller_id>/', views.SellersShowPrices.as_view(), name='sellers_show_prices'),
    path("add_price/<int:seller_id>", views.SellersAddPrice.as_view(), name='sellers_add_price'),
    path("delete_price/", views.SellersDeleteOrEditPrice.as_view(), name='sellers_delete_price'),
    path("payments_page/", views.PaymentsPage.as_view(), name='payments_page'),
    path("seller_payment/<int:seller_id>/", views.SellerPaymentsPage.as_view(), name='seller_payment_page'),
]