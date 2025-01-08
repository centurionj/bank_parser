from django.contrib import admin

from server.apps.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Админ панель для кредитов от лк банка"""

    list_display = (
        'title',
        'card_number',
        'phone_number',
        'created_at',
        'is_active',
        'has_temporary_code',
        'is_errored',
        'is_authenticated'
    )
    fields = (
        'title',
        'card_number',
        'phone_number',
        'temporary_code',
        'created_at',
        'is_active',
    )
    readonly_fields = ('created_at', 'session_cookies')
