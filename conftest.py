from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
import pytest

from cash.tests.factories import (
    UserFactory,
    CategoryFactory,
    TransactionFactory,
)


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def owner():
    return UserFactory()


@pytest.fixture
def api_client(owner):
    client = APIClient()
    refresh = RefreshToken.for_user(owner)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def transaction(owner):
    return TransactionFactory(user=owner)


@pytest.fixture
def transaction2(owner):
    return TransactionFactory(user=owner)
