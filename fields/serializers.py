from rest_framework import serializers

from .models import Field, Game, FavouriteField, Reservation
from .utils import get_time

from users.models import User

import datetime


class FieldSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(max_length=20, default=serializers.CurrentUserDefault())

    class Meta:
        model = Field
        fields = ('title', 'size', 'type', 'services', 'price', 'location', 'owner')


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('owner', 'reservation', 'price', 'title', 'description',
                  'location', 'field_type', 'match_type', 'start_date', 'start_time',
                  'duration', 'image', 'need_players', 'played_users', 'is_active')

    def validate(self, attrs):
        try:
            owner = User.objects.get(id=self.context['user'])
            attrs['owner'] = owner
        except User.DoesNotExist:
            raise serializers.ValidationError({'user': 'Такого пользователя не существует'})

        today = datetime.date.today()
        time = get_time()
        if attrs['start_date'] < today:
            raise serializers.ValidationError({'date': 'Дата бронирования не может быть раньше сегодняшней'})
        if attrs['start_date'] == today and attrs['start_time'] < time:
            raise serializers.ValidationError({'time': 'Время бронирование не может быть раньше текущего времени'})
        return attrs


# class GameSerializer(serializers.ModelSerializer):
#     join = serializers.BooleanField()
#
#     class Meta:
#         model = Game
#         fields = ('price', 'title', 'description',
#                   'location', 'field_type', 'match_type', 'start_date', 'start_time',
#                   'duration', 'image', 'join')


class JoinToGameSerializer(serializers.Serializer):
    game = serializers.SlugRelatedField(queryset=Game.objects.filter(
        start_date=datetime.date.today(), start_time=get_time()), slug_field='title')

    class Meta:
        fields = ('game',)

    def save(self, **kwargs):
        pass


class FavouriteFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteField
        fields = '__all__'


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

