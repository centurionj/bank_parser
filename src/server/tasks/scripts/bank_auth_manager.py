import requests

from server.settings.config import BASE_GO_API_URL


def authenticate_account_by_id(account_id: int) -> None:
    """
    Отправляет POST-запрос на BASE_GO_API_URL с JSON-данными.

    :param account_id: ID аккаунта для аутентификации
    :return: Ответ от сервера или ошибка
    :rtype: dict
    """

    try:
        payload = {'account_id': account_id}
        response = requests.post(f'{BASE_GO_API_URL}/auth/', json=payload)
        response.raise_for_status()  # Вызывает исключение для статусов 4xx/5xx
        return None

    except Exception as e:
        print('ERROR: ', str(e))
