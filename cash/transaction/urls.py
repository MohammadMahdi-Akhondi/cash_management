from django.urls import path

from . import apis


urlpatterns = [
    path('create', apis.CreateTransactionApi.as_view(), name='create_transaction'),
]
