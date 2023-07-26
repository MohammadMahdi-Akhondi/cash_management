from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_balance_for_multi_transaction(api_client, transaction, transaction2):
    url = reverse('api:transaction:balance')
    response = api_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('balance') != 0


@pytest.mark.django_db
def test_balance_for_no_transaction(api_client):
    url = reverse('api:transaction:balance')
    response = api_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('balance') == 0


@pytest.mark.django_db
def test_balance_unauthenticated_user(transaction):
    client = APIClient()
    url = reverse('api:transaction:balance')

    response = client.get(path=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_balance_with_invalid_method(api_client, transaction):
    url = reverse('api:transaction:balance')

    response = api_client.post(path=url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
