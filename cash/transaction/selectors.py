from django.contrib.auth import get_user_model
from .models import Category, Transaction
from django.db.models import QuerySet

from .filters import TransactionFilter

User = get_user_model()

def get_category_by_id(*, category_id: int) -> Category | None:

    try:
        category = Category.objects.get(id=category_id, deleted_at__isnull=True)
        return category

    except:
        return None


def get_transaction_by_id(*, transaction_id: int) -> Transaction | None:

    try:
        transaction = Transaction.objects.get(id=transaction_id, deleted_at__isnull=True)
        return transaction

    except:
        return None


def list_transaction(*,order_by: str = None, filters: dict, user: User) -> QuerySet[Transaction]:
    qs = Transaction.objects.filter(user=user, deleted_at__isnull=True)
    return TransactionFilter(filters, qs).qs.order_by(order_by)
