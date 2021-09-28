from rest_framework import authentication
from rest_framework import exceptions

from .models import User


def authenticate(request):
    phone = request.session['phone']

    if not phone:
        return None
    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('Пользователь не найден')

    return user
