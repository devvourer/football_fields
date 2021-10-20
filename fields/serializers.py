from rest_framework import serializers

from .models import Field, Game, FavouriteField, Reservation
from .utils import get_time

from users.models import User

import datetime
from dateutil.relativedelta import relativedelta


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
    period_weeks = serializers.IntegerField(allow_null=True)
    period_month = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Reservation
        fields = ('reservation_date', 'reservation_time',
                  'duration', 'field', 'user', 'period_weeks', 'period_month')

    def validate(self, attrs):

        try:
            user = User.objects.get(id=self.context['user'])
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError({'user': 'Такого пользователя не существует'})

        today = datetime.date.today()
        time = get_time()

        if attrs['reservation_date'] < today:
            raise serializers.ValidationError({'date': 'Дата бронирования не может быть раньше сегодняшней'})
        if attrs['reservation_date'] == today and attrs['reservation_time'] < time:
            raise serializers.ValidationError({'time': 'Время бронирование не может быть раньше текущего времени'})
        return attrs

    def create(self, validated_data):
        # print(validated_data['reservation_date'].day)
        copied_data = validated_data.copy()
        if validated_data['period_weeks']:
            for i in range(0, validated_data['period_weeks']):
                data = copied_data.copy()
                date = data['reservation_date']
                data['reservation_date'] = date + relativedelta(days=+7)
                copied_data['reservation_date'] = date + relativedelta(days=+7)

                try:
                    del data['period_weeks']
                    del data['period_month']
                    self.Meta.model.objects.create(**data)
                except Exception as e:
                    raise serializers.ValidationError('Fail to create reservation')

        if validated_data['period_month']:
            month = validated_data['period_month']
            new_date = validated_data['reservation_date'] + relativedelta(months=+month)
            d = new_date - validated_data['reservation_date']

            for i in range(0, d.days // 7):
                data = copied_data.copy()
                date = data['reservation_date']
                data['reservation_date'] = date + relativedelta(days=+7)
                copied_data['reservation_date'] = date + relativedelta(days=+7)

                try:
                    del data['period_month']
                    del data['period_weeks']
                    self.Meta.model.objects.create(**data)
                except Exception as e:
                    raise serializers.ValidationError('Fail to create reservation')
        try:
            del validated_data['period_month']
            del validated_data['period_weeks']
            return self.Meta.model.objects.create(**validated_data)
        except Exception as e:
            print(e)
            raise serializers.ValidationError('Reservation has not attribute')

