from datetime import timedelta

import requests
from django.utils import timezone

from server.apps.accounts.models import Account
from server.settings.config import (ACCOUNT_EXPIRATION_DELTA_DAY,
                                    ACCOUNT_LIFETIME_MINUTES, BASE_GO_API_URL)


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

    try:
        payload = {'account_ids': [account.id for account in expired_accounts]}
        response = requests.post(f'{BASE_GO_API_URL}/account/auth/', json=payload)
        response.raise_for_status()  # Вызывает исключение для статусов 4xx/5xx
        expired_accounts.delete()
        return None

    except Exception as e:
        print('ERROR: ', str(e))
