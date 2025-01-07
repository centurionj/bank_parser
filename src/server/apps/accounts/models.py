import json

from django.db import models

from server.apps.accounts.validators import (validate_card_number,
                                             validate_phone_number)


class Account(models.Model):
    """Модель кредитов от лк банка."""

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
    temporary_code = models.CharField('Одноразовый код', max_length=4, null=True, blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=False)
    has_temporary_code = models.BooleanField(default=False)
    session_cookies = models.TextField('Cookies сессии', null=True, blank=True)

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['-created_at', 'is_active', 'has_temporary_code', 'is_authenticated']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.temporary_code:
            self.has_temporary_code = True

        super(Account, self).save(*args, **kwargs)

    def set_cookies(self, cookies):
        """Сохранить cookies в текстовом формате."""

        self.session_cookies = json.dumps(cookies)
        self.save()

    def get_cookies(self):
        """Загрузить cookies из текстового формата."""

        return json.loads(self.session_cookies) if self.session_cookies else None
