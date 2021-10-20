from django.conf import settings
from users.models import User

import requests
import uuid


def send_request_to_game(sender: str, receiver: str, game_id: int) -> None:
    sender = User.objects.get(phone=sender)
    receiver = User.objects.get(phone=receiver)

    accept_url = f'http://127.0.0.1:8000/fields/game/{game_id}/{sender.id}'

    body = {
        'login': 'Iminov',
        'pwd': '9KtUJ84_',
        'id': str(uuid.uuid4())[0:10],
        'sender': 'Test',
        'text': f'{sender} хочет присоединиться к вашей игре'
                f'{accept_url}  - Принять запрос',
        'phone': receiver.phone,
        'test': 1
    }

    print(body)
    response = requests.post(settings.SMS_API_URL, json=body)
    print(response.status_code)


def send_notification(phone: str) -> None:
    body = {
        'login': 'Iminov',
        'pwd': '9KtUJ84_',
        'id': str(uuid.uuid4())[0:10],
        'sender': 'Test',
        'text': f'У вас недостаточно средств для бронирования футбольного поля, пополните баланс в течении 12 часов,'
                f' либо бронь станет не активной',
        'phone': phone,
        'test': 1
    }

    response = requests.post(settings.SMS_API_URL, json=body)
    print(body)
    print(response.status_code)

