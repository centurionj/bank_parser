from django.db import models

from server.apps.accounts.validators import (validate_card_number,
                                             validate_phone_number)


class Account(models.Model):
    """Модель кредитов от лк банка"""

    title = models.CharField('Название', max_length=25, null=True, blank=True)
    card_number = models.CharField(
        'Номер карты',
        max_length=16,
        null=False,
        blank=False,
        validators=[validate_card_number]
    )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=11,
        null=False,
        blank=False,
        validators=[validate_phone_number]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['created_at', 'is_active']

    def __str__(self):
        return str(self.title)
