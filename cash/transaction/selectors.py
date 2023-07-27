from django.db.models import Case, When, F, Sum, IntegerField
from django.contrib.auth import get_user_model
from .models import Category, Transaction
from django.db.models import QuerySet

from .filters import TransactionFilter

User = get_user_model()

def get_category_by_id(*, category_id: int) -> Category | None:
    """
    Returns the Category object with the given category_id if it exists and is not deleted.
    Returns None otherwise.
    
    Args:
        category_id (int): The ID of the desired Category object.
    
    Returns:
        Optional[Category]: The Category object with the given category_id, or None if it doesn't exist or is deleted.
    """

    try:
        category = Category.objects.get(id=category_id, deleted_at__isnull=True)
        return category

    except:
        return None


def get_transaction_by_id(*, transaction_id: int) -> Transaction | None:
    """
    Returns the Transaction object with the given transaction_id if it exists and is not deleted.
    Returns None otherwise.
    
    Args:
        transaction_id (int): The ID of the desired Transaction object.
    
    Returns:
        Optional[Transaction]: The Transaction object with the given transaction_id, or None if it doesn't exist or is deleted.
    """

    try:
        transaction = Transaction.objects.get(id=transaction_id, deleted_at__isnull=True)
        return transaction

    except:
        return None


def list_transaction(*, order_by: str = 'date', filters: dict, user: User) -> QuerySet[Transaction]:
    """
    Returns a QuerySet of Transaction objects that belong to the given user and match the given filters.
    The QuerySet is ordered by the field specified in order_by, if provided.
    
    Args:
        order_by (str): The field to order the QuerySet by. Defaults to 'date'.
        filters (dict): A dictionary of filters to apply to the QuerySet.
        user (User): The User object whose Transactions to retrieve.
    
    Returns:
        QuerySet[Transaction]: The QuerySet of Transaction objects that belong to the given user and match the given filters.
    """

    qs = Transaction.objects.filter(user=user, deleted_at__isnull=True)
    return TransactionFilter(filters, qs).qs.order_by(order_by)


def get_balance(*, user: User) -> int:
    """
    Returns the balance of the given user based on their Transactions.
    The balance is the sum of all income Transactions minus the sum of all expense Transactions.
    
    Args:
        user (User): The User object whose balance to retrieve.
    
    Returns:
        int: The balance of the given user.
    """

    return Transaction.objects.filter(user=user).annotate(
        value=Case(
            When(transaction_type='E', then=-1 * F('amount')),
            When(transaction_type='I', then=F('amount')),
            output_field=IntegerField(),
        ),
    ).aggregate(balance=Sum('value'))['balance'] or 0
