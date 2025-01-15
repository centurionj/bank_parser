from django.db import models

from server.apps.accounts.validators import (validate_card_number,
                                             validate_phone_number)


class Account(models.Model):
    """Модель кредитов от лк банка."""

    title = models.CharField('Название', max_length=25, null=True, blank=True, help_text='Не обязательное поле')
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
    temporary_code = models.CharField('Одноразовый код', max_length=4, null=True, blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=False)
    has_temporary_code = models.BooleanField(default=False)
    is_errored = models.BooleanField(default=False)
    session_cookies = models.TextField('Cookies session', null=True, blank=True)
    user_agent = models.TextField('Google user agent', null=True, blank=True)

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['-created_at', 'is_active', '-is_errored', 'is_authenticated']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.temporary_code:
            self.has_temporary_code = True

        super(Account, self).save(*args, **kwargs)
