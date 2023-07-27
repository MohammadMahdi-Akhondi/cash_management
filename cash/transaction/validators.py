from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Transaction
from . import selectors


def validate_transaction_id(transaction_id) -> Transaction:
    """
    Validates that a Transaction object with the given transaction_id exists and is not deleted.
    Raises a ValidationError if the Transaction is not found or is deleted.
    Returns the Transaction object if it exists and is not deleted.
    
    Args:
        transaction_id: The ID of the Transaction object to validate.
    
    Returns:
        Transaction: The validated Transaction object.
    
    Raises:
        ValidationError: If the Transaction is not found or is deleted.
    """

    transaction = selectors.get_transaction_by_id(transaction_id=transaction_id)
    if not transaction:
        raise ValidationError({'transaction_id': _('transaction not found')})

    return transaction
