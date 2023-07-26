import pytest

from cash.transaction.selectors import list_transaction


@pytest.mark.django_db
def test_list_transaction_with_valid_data(transaction, owner):
    order_by = 'amount'
    filters = {
        'date': transaction.date,
        'category__in': f'{transaction.category.id}',
        'date__range': 'today',
    }
    qs = list_transaction(order_by=order_by, filters=filters, user=owner)

    assert qs.first().id == transaction.id
