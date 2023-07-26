import pytest

from cash.transaction.services import delete_transaction


@pytest.mark.django_db
def test_delete_transaction(transaction):
    delete_transaction(transaction=transaction)

    assert transaction.deleted_at != None
