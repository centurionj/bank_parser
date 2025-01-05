from rest_framework import serializers

from server.apps.accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer для модели Account"""

    class Meta:
        model = Account
        fields = ['id', 'title', 'card_number', 'phone_number', 'created_at', 'is_active']
