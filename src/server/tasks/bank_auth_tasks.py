from typing import Sequence

from celery import shared_task
from django.apps import apps

from server.tasks.scripts.bank_auth_manager import authenticate


@shared_task(bind=True)
def bank_authenticate_by_id_task(self, account_id: int):
    """Первичный вход в лк банка"""

    Account = apps.get_model('accounts', 'Account')
    account: Account = Account.objects.get(id=account_id)

    authenticate(account)


@shared_task(bind=True)
def bank_authenticate_all_accounts_task(self):
    """Вход в лк банка для поддержания сессии"""

    Account = apps.get_model('accounts', 'Account')
    accounts: Sequence[Account] = Account.objects.filter(
        is_active=True,
        is_authenticated=True,
    )

    for account in accounts:
        authenticate(account)
