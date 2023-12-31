from django.test import Client
from rest_framework import status
from django.urls import reverse
from datetime import datetime
import pytest


@pytest.mark.django_db
def test_create_with_valid_data(api_client, category):
    url = reverse('api:transaction:create_transaction')
    date = datetime.now().date()
    data = {
        'amount': 150,
        'transaction_type': 'I',
        'category': category.id,
        'date': date,
    }

    response = api_client.post(path=url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get('amount') == 150
    assert response.data.get('transaction_type') == 'I'
    assert response.data.get('category') == category.id
    assert response.data.get('date') == str(date)


@pytest.mark.django_db
def test_create_with_invalid_data(api_client):
    url = reverse('api:transaction:create_transaction')
    data = {
        'amount': 150,
        'transaction_type': 'F',
        'category': 5,
        'date': datetime.now().date(),
    }

    response = api_client.post(path=url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get('id') == None


@pytest.mark.django_db
def test_update_with_unauthenticated_user():
    client = Client()
    url = reverse('api:transaction:create_transaction')

    response = client.post(path=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED        
