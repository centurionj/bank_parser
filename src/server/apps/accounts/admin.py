from django.contrib import admin
from django.contrib.auth.models import Group, User

from server.apps.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Админ панель для кредитов от лк банка"""

    list_display = ('title', 'card_number', 'phone_number', 'created_at', 'is_active')
    fields = ('title', 'card_number', 'phone_number', 'created_at', 'is_active')
    readonly_fields = ('created_at',)


admin.site.unregister(Group)
