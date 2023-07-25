from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest


User = get_user_model()

@pytest.fixture
def api_client():
    client = APIClient()
    user = User.objects.create_user(username='mahdi', password='strong_password')
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
