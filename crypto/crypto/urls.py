from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('login/', include('registered.urls')),
    path('', include('main.urls')),
]
