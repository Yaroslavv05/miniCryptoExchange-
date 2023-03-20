from django.urls import path, include

urlpatterns = [
    path('login', include('registered.urls')),
]
