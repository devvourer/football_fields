from .models import User

import requests
import uuid


def send_activation_code(phone: str) -> None:
    url = 'https://smspro.nikita.kg/api/message'

    user = User.objects.get(phone=phone)
    code = user.code

    body = {
        'login': 'Iminov',
        'pwd': '9KtUJ84_',
        'id': str(uuid.uuid4())[0:10],
        'sender': 'Тест',
        'text': str(code),
        'phone': phone,
        'test': 1
    }
    print(code)
    response = requests.post(url, json=body)


