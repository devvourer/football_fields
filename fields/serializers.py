from rest_framework import serializers

from .models import Field, Game

from reservations.utils import get_time
from users.models import User

import datetime


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = ('title', 'size', 'type', 'service', 'price', 'location', 'owner')


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('owner', 'price', 'title', 'description',
                  'location', 'field_type', 'match_type', 'start_date', 'start_time',
                  'duration', 'image', 'need_players', 'played_users', 'is_active')

    def validate(self, attrs):
        try:
            owner = User.objects.get(id=self.context['phone'])
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
