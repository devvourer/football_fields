from django.db import models
from users.models import User

FIELD_TYPE = (
    ('turf', 'газон'),
    ('grass', 'трава'),
    ('indoor', 'крытый'),
    ('sand', 'песок'),
    ('beach', 'пляж')
)


class Service(models.Model):
    SERVICES = (
        ('water', 'вода'),
        ('cloakroom', 'раздевалка'),
        ('shower', 'душ'),
    )
    name = models.CharField(max_length=30, choices=SERVICES)

    def __str__(self):
        return self.name

class Field(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    title = models.CharField(max_length=255)
    size = models.IntegerField()
    type = models.CharField(choices=FIELD_TYPE, max_length=20)
    services = models.ManyToManyField(Service)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # location = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

    def __str__(self):
        return self.title


class Image(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/field_images')


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, related_name='reservations')

    # reservation_date = models.DateField()
    # reservation_time = models.TimeField()
    # duration = models.DecimalField(max_digits=2, decimal_places=1)

    paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        ordering = ()

    def __str__(self):
        return f'{self.user} : {self.field} : {self.reservation_date}'


class Game(models.Model):
    MATCH_TYPES = (
        ('friendly', 'товарищеский'),
        ('competitive', 'соревновательный'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='game')
    played_users = models.ManyToManyField(User, related_name='played_games')
    price = models.DecimalField(max_digits=7, decimal_places=1)

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=255)
    field_type = models.CharField(choices=FIELD_TYPE, max_length=100)
    match_type = models.CharField(choices=MATCH_TYPES, max_length=100)
    need_players = models.IntegerField(default=2)

    start_date = models.DateField()
    start_time = models.TimeField()

    duration = models.DecimalField(max_digits=2, decimal_places=1)
    image = models.ImageField(upload_to='media/game_detail', null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return f'{self.title}'


class FavouriteField(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, unique=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} : {self.field}'
