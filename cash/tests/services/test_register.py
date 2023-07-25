from django.contrib.auth.hashers import check_password
import pytest

from cash.user.services import register


@pytest.mark.django_db
def test_register():
    user = register(username='foo', password='admin')

    assert user.username == 'foo'
    assert check_password('admin', user.password)
