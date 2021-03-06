from django.conf import settings
from .models import User

import requests
import uuid


def send_code(phone: str) -> None:
    user = User.objects.get(phone=phone)
    code = user.code

    body = {
        'login': 'Iminov',
        'pwd': '9KtUJ84_',
        'id': str(uuid.uuid4())[0:10],
        'sender': 'Тест',
        'text': f'{str(code)}',
        'phone': phone,
        'test': 1
    }

    print(code)
    response = requests.post(settings.SMS_API_URL, json=body)
    print(response.status_code)


def send_code_to_reset_pwd(phone: str, code: int) -> None:
    body = {
        'login': 'Iminov',
        'pwd': '9KtUJ84_',
        'id': str(uuid.uuid4())[0:10],
        'sender': 'Тест',
        'text': f'http://127.0.0.1:8000/users/{phone}/{str(code)}/reset/'
                f'Перейдите по ссылке для сбора пароля',
        'phone': phone,
        'test': 1
    }
    print(body)
    response = requests.post(settings.SMS_API_URL, json=body)
    print(response)

