from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest


User = get_user_model()

@pytest.fixture
def api_client():
    client = APIClient()
    return client
