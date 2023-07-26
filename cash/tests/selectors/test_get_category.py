import pytest

from cash.transaction.selectors import get_category_by_id


@pytest.mark.django_db
def test_get_transaction_with_valid_data(category):
    obj = get_category_by_id(category_id=category.id)

    assert obj.id == category.id


@pytest.mark.django_db
def test_get_transaction_with_invalid_data():
    obj = get_category_by_id(category_id=100)

    assert obj == None
