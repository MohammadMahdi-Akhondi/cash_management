from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client
from rest_framework import status
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_delete_with_valid_data(api_client, transaction):
    url = reverse('api:transaction:delete_transaction', args=[transaction.id])
    response = api_client.delete(path=url)
    transaction.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert transaction.deleted_at != None


@pytest.mark.django_db
def test_delete_with_unauthenticated_user(transaction):
    client = Client()
    url = reverse('api:transaction:delete_transaction', args=[transaction.id])

    response = client.delete(path=url)
    transaction.refresh_from_db()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert transaction.deleted_at == None


@pytest.mark.django_db
def test_delete_with_unauthorized_user(api_client, transaction, user):
    url = reverse('api:transaction:delete_transaction', args=[transaction.id])
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    response = api_client.delete(path=url)
    transaction.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert transaction.deleted_at == None


@pytest.mark.django_db
def test_delete_with_invalid_method(api_client, transaction):
    url = reverse('api:transaction:delete_transaction', args=[transaction.id])

    response = api_client.post(path=url)
    transaction.refresh_from_db()

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert transaction.deleted_at == None
