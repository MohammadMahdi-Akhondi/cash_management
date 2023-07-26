from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Transaction
from . import selectors

def validate_transaction_id(transaction_id) -> Transaction:
    transaction = selectors.get_transaction_by_id(transaction_id=transaction_id)
    if not transaction:
        raise ValidationError({'transaction_id': _('transaction not found')})

    return transaction
