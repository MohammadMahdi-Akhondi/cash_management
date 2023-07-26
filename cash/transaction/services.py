
from django.contrib.auth import get_user_model
from .models import Transaction, Category
from datetime import datetime


User = get_user_model()

def create_transaction(*,
        user: User, 
        amount: int, 
        transaction_type: str,
        category: Category,
        date:datetime.date) -> Transaction:

    return Transaction.objects.create(
        user=user,
        amount=amount,
        transaction_type=transaction_type,
        category=category,
        date=date,
    )


def update_transaction(*,
        transaction: Transaction,
        amount: int, 
        transaction_type: str,
        category: Category,
        date:datetime.date) -> Transaction:

    transaction.amount = amount
    transaction.transaction_type = transaction_type
    transaction.category = category
    transaction.date = date
    transaction.save()
    return transaction


def delete_transaction(*, transaction: Transaction) -> None:
    transaction.deleted_at = datetime.now()
    transaction.save()
