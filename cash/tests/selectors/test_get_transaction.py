import pytest

from cash.transaction.selectors import get_transaction_by_id


@pytest.mark.django_db
def test_get_transaction_with_valid_data(transaction):
    obj = get_transaction_by_id(transaction_id=transaction.id)

    assert obj.id == transaction.id


@pytest.mark.django_db
def test_get_transaction_with_invalid_data():
    obj = get_transaction_by_id(transaction_id=100)

    assert obj == None
