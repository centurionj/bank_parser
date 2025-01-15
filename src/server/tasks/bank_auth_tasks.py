from celery import shared_task

from server.tasks.scripts.bank_auth_manager import authenticate_account_by_id


@shared_task(bind=True)
def authenticate_account_by_id_task(self, account_id: int):
    """Отправляет запрос на авторизацию в личном кабинете."""

    authenticate_account_by_id(account_id)
