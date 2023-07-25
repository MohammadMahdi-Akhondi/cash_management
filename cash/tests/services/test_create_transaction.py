from datetime import datetime
import pytest

from cash.transaction.services import create_transaction


@pytest.mark.django_db
def test_create_transaction(user, category):
    data = {
        'amount': 125,
        'transaction_type': 'I',
        'date': datetime.now().date()
    }
    transaction = create_transaction(user=user, category=category, **data)

    assert transaction.amount == 125
    assert transaction.transaction_type == 'I'
    assert transaction.date == data.get('date')
