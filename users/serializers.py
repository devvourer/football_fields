from rest_framework import serializers
from .models import User, Owner, Profile

from reservations.utils import CurrentUser


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


class ResetPhoneSerializer(serializers.Serializer):
    new_phone = serializers.RegexField(regex=r'^\+?1?\d{9,15}$',
                                   error_messages={'invalid phone': 'Неверный формат номера !'})
    password = serializers.CharField(max_length=255)

    class Meta:
        fields = ('new_phone', 'password')

    def validate(self, attrs):
        user = self.context['user']

        if user.password == attrs['password']:
            return attrs
        else:
            raise serializers.ValidationError({'password': 'пароль не совпадает'})


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.RegexField(regex=r'^\+?1?\d{9,15}$',
                                   error_messages={'invalid phone': 'Неверный формат номера !'})

    class Meta:
        fields = ('phone',)


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=255)
    password1 = serializers.CharField(max_length=255)

    class Meta:
        fields = ('password', 'password1')

    def validate(self, attrs):

        if attrs['password1'] != attrs['password']:
            raise serializers.ValidationError({'password': 'пароли не совпадают'})

        return attrs


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.RegexField(regex=r'^\+?1?\d{9,15}$',
                                  error_messages={'invalid phone': 'Неверный формат номера !'},
                                  default=CurrentUser())

    class Meta:
        model = Profile
        fields = ('user', 'avatar', 'age', 'name',
                  'weight', 'height', 'foot', 'favourite_club', 'jersey_number',
                  'position_primary', 'position_secondary')
