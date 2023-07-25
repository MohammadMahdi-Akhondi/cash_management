from django.urls import path

from .import apis


urlpatterns = [
    path('register/', apis.RegisterApi.as_view(), name='register'),
]
