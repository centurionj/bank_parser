from celery import shared_task

from server.tasks.scripts.account_manager import (
    change_account_status_by_date, delete_accounts_by_date)


@shared_task
def change_account_status_task():
    """Изменяет активность аккаунта по истечению срока"""

    change_account_status_by_date()


@shared_task
def delete_account_task():
    """Удаляет аккаунт по истечению срока"""

    delete_accounts_by_date()
