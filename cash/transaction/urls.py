from django.urls import path

from . import apis


urlpatterns = [
    path('create/', apis.CreateTransactionApi.as_view(), name='create_transaction'),
    path('update/<int:transaction_id>/', apis.UpdateTransactionApi.as_view(), name='update_transaction'),
]
