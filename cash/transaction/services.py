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

    """
    Creates a new Transaction object with the given attributes and saves it to the database.
    Returns the created Transaction object.
    
    Args:
        user (User): The User who owns the new Transaction.
        amount (int): The amount of the new Transaction.
        transaction_type (str): The type of the new Transaction ('I' for income, 'E' for expense).
        category (Category): The Category of the new Transaction.
        date (datetime.date): The date of the new Transaction.
    
    Returns:
        Transaction: The newly created Transaction object.
    """

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

    """
    Updates the attributes of an existing Transaction object and saves it to the database.
    Returns the updated Transaction object.
    
    Args:
        transaction (Transaction): The Transaction object to update.
        amount (int): The new amount of the Transaction.
        transaction_type (str): The new type of the Transaction ('I' for income, 'E' for expense).
        category (Category): The new Category of the Transaction.
        date (datetime.date): The new date of the Transaction.
    
    Returns:
        Transaction: The updated Transaction object.
    """

    transaction.amount = amount
    transaction.transaction_type = transaction_type
    transaction.category = category
    transaction.date = date
    transaction.save()
    return transaction


def delete_transaction(*, transaction: Transaction) -> None:
    """
    Marks an existing Transaction object as deleted and saves it to the database.
    
    Args:
        transaction (Transaction): The Transaction object to delete.
    """

    transaction.deleted_at = datetime.now()
    transaction.save()
