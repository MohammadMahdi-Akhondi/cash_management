from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client
from rest_framework import status
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_detail_with_valid_data(api_client, transaction):
    url = reverse('api:transaction:detail_transaction', args=[transaction.id])
    refresh = RefreshToken.for_user(transaction.user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    response = api_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_detail_with_unauthenticated_user(transaction):
    client = Client()
    url = reverse('api:transaction:detail_transaction', args=[transaction.id])

    response = client.get(path=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_detail_with_unauthorized_user(api_client, transaction):
    url = reverse('api:transaction:detail_transaction', args=[transaction.id])

    response = api_client.get(path=url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_detail_with_invalid_method(api_client, transaction):
    url = reverse('api:transaction:detail_transaction', args=[transaction.id])

    response = api_client.post(path=url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
