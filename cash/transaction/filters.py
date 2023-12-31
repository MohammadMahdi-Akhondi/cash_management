from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django_filters import (
    DateRangeFilter,
    CharFilter,
    FilterSet,
)

from .models import Transaction


class TransactionFilter(FilterSet):
    """
    Custom filter class for filtering Transaction objects by date range, category, and amount range.
    """

    date__range = DateRangeFilter(field_name='date')
    category__in = CharFilter(method='filter_category__in')
    amount__range = CharFilter(method='filter_amount__range')

    def filter_category__in(self, queryset, name, value):
        limit = 10
        categories = value.split(',')
        categories = [int(category) for category in categories]
        if len(categories) > limit:
            raise ValidationError({'category__in': _(f'you can\'t more add more than {limit} categories')})

        return queryset.filter(category__id__in=categories)

    def filter_amount__range(self, queryset, name, value):
        limit = 2
        amount__range = value.split(',')
        if len(amount__range) != limit:
            raise ValidationError(_('Please just add two amount with , in the middle'))

        try:
            amount__range = [int(amount) for amount in amount__range]

        except ValueError:
            raise ValidationError(_('Please enter valid integer'))
        
        from_amount, to_amount = amount__range

        return queryset.filter(amount__range=(from_amount, to_amount))

    class Meta:
        model = Transaction
        fields = (
            'date',
            'transaction_type',
        )
