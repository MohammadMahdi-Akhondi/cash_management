from .models import Category, Transaction


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
