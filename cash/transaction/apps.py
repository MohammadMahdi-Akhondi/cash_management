from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class TransactionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cash.transaction'
    verbose_name = _('Transaction management')
