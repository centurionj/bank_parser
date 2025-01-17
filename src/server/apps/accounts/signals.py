from django.db.models.signals import post_save
from django.dispatch import receiver

from server.apps.accounts.models import Account
from server.settings.config import CELERY_TASK_DELAY_SEC
from server.tasks.bank_auth_tasks import authenticate_account_by_id_task

@receiver(post_save, sender=Account)
def trigger_bank_auth_task(sender, instance, created, **kwargs):
    if created and not instance.is_authenticated:
        authenticate_account_by_id_task.apply_async(args=[instance.id], countdown=CELERY_TASK_DELAY_SEC)