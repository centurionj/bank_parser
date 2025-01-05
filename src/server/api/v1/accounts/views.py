from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from server.apps.accounts.models import Account

from .serializers import AccountSerializer


class AccountDetailView(RetrieveAPIView):
    """
    DetailView для получения информации об аккаунте
    по id, card_number или phone_number.
    """

    permission_classes = [AllowAny]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @swagger_auto_schema(
        operation_summary="Получить детали аккаунта",
        operation_description=(
                "Возвращает детали аккаунта на основе id, номера карты (card_number) "
                "или номера телефона (phone_number)."
        ),
        manual_parameters=[
            openapi.Parameter(
                name="lookup_value",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description="ID (число), номер карты (16 цифр), или номер телефона (11 цифр)",
                required=True,
            )
        ],
        responses={
            200: AccountSerializer,
            404: "Аккаунт не найден."
        }
    )
    def get_object(self):
        lookup_value = self.kwargs.get('lookup_value')
        filters = {}

        if lookup_value.isdigit():
            if len(lookup_value) == 11:
                filters['phone_number'] = lookup_value
            elif len(lookup_value) == 16:
                filters['card_number'] = lookup_value
            else:
                filters['id'] = lookup_value

        obj = self.get_queryset().filter(**filters).first()

        if not obj:
            raise NotFound('Аккаунт не найден.')

        return obj
