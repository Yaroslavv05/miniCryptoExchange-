from django.urls import path
from .views import index,chart

urlpatterns = [
    path('', index),
    path('chart/', chart)
]
