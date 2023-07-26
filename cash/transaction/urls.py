from django.urls import path

from . import apis


urlpatterns = [
    path('list/', apis.ListTransactionApi.as_view(), name='list_transaction'),
    path('create/', apis.CreateTransactionApi.as_view(), name='create_transaction'),
    path('update/<int:transaction_id>/', apis.UpdateTransactionApi.as_view(), name='update_transaction'),
    path('detail/<int:transaction_id>/', apis.DetailTransactionApi.as_view(), name='detail_transaction'),
    path('delete/<int:transaction_id>/', apis.DeleteTransactionApi.as_view(), name='delete_transaction'),
]
