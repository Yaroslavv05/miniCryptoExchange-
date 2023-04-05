from django.urls import path
from .views import *

urlpatterns = [
    path('', spot, name='spot'),
    path('spot_coin/', spot_coin, name='spot_coin'),
    path('spot_trade/get_price_change/', get_price_change, name='get_price_change'),
    path('pay/', pay, name='pay'),
    path('paid/', paid, name='paid')
]