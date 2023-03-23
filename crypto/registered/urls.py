from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', user_register, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin/', user_login, name='signin'),
    path('account/', account, name='account'),
    path('verification/', KYC, name='kyc'),
    path('account_verification/', account_kyc, name='account_kyc')
]