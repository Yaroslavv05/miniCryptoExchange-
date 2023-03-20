from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('signup', include('registered.urls')),
    path('', include('main.urls')),
]
