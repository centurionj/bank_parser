import re

from django.core.exceptions import ValidationError


def validate_card_number(value):
    """
    Валидатор для проверки номера карты.
    Номер карты должен состоять из 16 цифр.
    """
    if not re.fullmatch(r'\d{16}', value):
        raise ValidationError('Номер карты должен содержать ровно 16 цифр.')


def validate_phone_number(value):
    """
    Валидатор для проверки номера телефона.
    Номер телефона должен состоять из 11 цифр и начинаться с 7.
    """
    if not re.fullmatch(r'7\d{10}', value):
        raise ValidationError('Номер телефона должен содержать 11 цифр и начинаться с "7".')
