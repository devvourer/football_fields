from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, label='password',
                                     required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, label='password',
                                     required=True, style={'input_type': 'password'})
    phone = serializers.RegexField(regex=r'^\+?1?\d{9,15}$',
                                   error_messages={'invalid phone': 'Неверный формат номера !'})

    class Meta:
        model = User
        fields = ('phone', 'password', 'password2')

    def validate(self, attrs):
        phone = attrs['phone']
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Пароли не совпадают!'})

        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'phone': 'Такой номер телефона уже зарегистрирован'})

        del attrs['password2']
        return attrs


class UserActivateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        code = attrs['code']
        if len(code) < 6:
            raise serializers.ValidationError({'code': 'Код должен содержать 6 цифр'})
        return attrs

    class Meta:
        fields = ('code',)


class LoginSerializer(serializers.Serializer):
    phone = serializers.RegexField(regex=r'^\+?1?\d{9,15}$',
                                   error_messages={'invalid phone': 'Неверный формат номера !'})
    password = serializers.CharField(max_length=255)

    class Meta:
        fields = ('phone', 'password')






