from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client
from rest_framework import status
from django.urls import reverse
from datetime import datetime
import pytest


@pytest.mark.django_db
def test_update_with_valid_data(api_client, transaction):
    url = reverse('api:transaction:update_transaction', args=[transaction.id])
    refresh = RefreshToken.for_user(transaction.user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    data = {
        'amount': 300,
        'transaction_type': 'I',
        'category': transaction.category.id,
        'date': datetime.now().date(),
    }

    response = api_client.put(path=url, data=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_with_invalid_data(api_client, transaction):
    url = reverse('api:transaction:update_transaction', args=[transaction.id])
    data = {
        'amount': -10,
        'transaction_type': 'I',
        'category': 5,
        'date': datetime.now().date(),
    }
    refresh = RefreshToken.for_user(transaction.user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    response = api_client.put(path=url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_with_unauthenticated_user(transaction):
    client = Client()
    url = reverse('api:transaction:update_transaction', args=[transaction.id])

    response = client.post(path=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_with_unauthorized_user(api_client, transaction):
    url = reverse('api:transaction:update_transaction', args=[transaction.id])
    data = {
        'amount': 300,
        'transaction_type': 'I',
        'category': transaction.category.id,
        'date': datetime.now().date(),
    }

    response = api_client.put(path=url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
