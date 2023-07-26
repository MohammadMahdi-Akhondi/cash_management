import pytest

from cash.transaction.selectors import get_balance


@pytest.mark.django_db
def test_get_balance(owner, user, transaction, transaction2):

    balance = 0

    if transaction.transaction_type == 'I':
        balance += int(transaction.amount)

    else:
        balance -= int(transaction.amount)

    if transaction2.transaction_type == 'I':
        balance += int(transaction2.amount)

    else:
        balance -= int(transaction2.amount)

    assert get_balance(user=user) == 0
    assert get_balance(user=owner) == balance
