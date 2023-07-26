from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from cash.common.models import BaseModel


User = get_user_model()

class Category(BaseModel):
    name = models.CharField(
        max_length=150,
        verbose_name=_('name')
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self) -> str:
        return self.name


class Transaction(BaseModel):

    class TypeChoices(models.TextChoices):
        INCOME = 'I', _('income')
        EXPENSE = 'E', _('expense')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    amount = models.PositiveIntegerField(verbose_name=_('amount'))
    transaction_type = models.CharField(
        max_length=1,
        choices=TypeChoices.choices,
        verbose_name=_('type')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        verbose_name=_('category')
    )
    date = models.DateField(verbose_name=_('date'))


    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')


    def __str__(self) -> str:
        return str(self.user) + ' ' + str(self.amount)
