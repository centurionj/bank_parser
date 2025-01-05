from datetime import timedelta

from django.utils import timezone

from server.apps.accounts.models import Account
from server.settings.config import (ACCOUNT_EXPIRATION_DELTA_DAY,
                                    ACCOUNT_LIFETIME_MINUTES)


def change_account_status_by_date():
    """Изменяет активность аккаунта по истечению срока"""

    now = timezone.now()
    accounts_to_deactivate = Account.objects.filter(
        is_active=True,
        created_at__lte=now - timedelta(minutes=ACCOUNT_LIFETIME_MINUTES)
    )
    accounts_to_deactivate.update(is_active=False)


def delete_accounts_by_date():
    """Удаляет аккаунт по истечению срока"""

    now = timezone.now()
    expired_accounts = Account.objects.filter(created_at__lte=now - timedelta(days=ACCOUNT_EXPIRATION_DELTA_DAY))
    expired_accounts.delete()
