from datetime import datetime
import pytest

from cash.transaction.services import update_transaction


@pytest.mark.django_db
def test_update_transaction(transaction, category):
    data = {
        'transaction': transaction,
        'amount': 125,
        'category': category,
        'transaction_type': 'E',
        'date': datetime.now().date()
    }
    transaction = update_transaction(**data)

    assert transaction.amount == 125
    assert transaction.transaction_type == 'E'
    assert transaction.date == data.get('date')