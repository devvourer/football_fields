from rest_framework import serializers

from .models import Reservation
from .utils import get_time

from fields.models import Field
from users.models import User

import datetime


class ReservationSerializer(serializers.Serializer):
    reservation_date = serializers.DateField()
    reservation_time = serializers.TimeField()
    duration = serializers.DecimalField(max_digits=2, decimal_places=1)
    field = serializers.SlugRelatedField(queryset=Field.objects.all(), slug_field='title')

    class Meta:
        model = Reservation
        fields = ('reservation_date', 'reservation_time', 'duration', 'field', 'user')

    def validate(self, attrs):

        try:
            user = User.objects.get(id=self.context['user'])
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError({'user': 'Такого пользователя не существует'})

        today = datetime.date.today()
        time = get_time()
        print(time)
        if attrs['reservation_date'] < today:
            raise serializers.ValidationError({'date': 'Дата бронирования не может быть раньше сегодняшней'})
        if attrs['reservation_date'] == today and attrs['reservation_time'] < time:
            raise serializers.ValidationError({'time': 'Время бронирование не может быть раньше текущего времени'})
        return attrs

    def create(self, validated_data):
        try:
            return self.Meta.model.objects.create(**validated_data)
        except Exception as e:
            print(e)
            raise serializers.ValidationError('Reservation has not attribute')

