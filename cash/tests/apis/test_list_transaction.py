from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client
from rest_framework import status
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_list_with_valid_data(api_client, transaction):
    url = reverse('api:transaction:list_transaction') + \
        f'?date={transaction.date}' + \
        f'&category__in={transaction.category.id}' + \
        f'&date__range=today&order_by=amount'
    
    response = api_client.get(path=url)

    assert response.data['results'][0]['id'] == transaction.id
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('limit') == 10
    assert response.data.get('count') == 1


@pytest.mark.django_db
def test_list_with_invalid_data(api_client):
    url = reverse('api:transaction:list_transaction') + \
        f'?date=2023-11-04' + \
        f'&category__in=100' + \
        f'&date__range=tomorrow&order_by=amount'

    response = api_client.get(path=url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_list_with_unauthenticated_user():
    client = Client()
    url = reverse('api:transaction:list_transaction')

    response = client.get(path=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_detail_with_invalid_method(api_client):
    url = reverse('api:transaction:list_transaction')

    response = api_client.post(path=url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
