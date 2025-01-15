from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.accounts'
    verbose_name = 'Аккаунты'

    def ready(self):
        import server.apps.accounts.signals
