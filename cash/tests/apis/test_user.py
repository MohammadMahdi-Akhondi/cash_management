from rest_framework import status
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_register_with_invalid_data(api_client):
    url = reverse('api:user:register')
    data = {
        'username': 'admin',
        'password': 'admin',
    }

    response = api_client.post(
        path=url, data=data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_with_valid_data(api_client):
    url = reverse('api:user:register')
    data = {
        'username'        : 'admin',
        'password'        : 'strong_password',
        'confirm_password': 'strong_password',
    }

    response = api_client.post(path=url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
