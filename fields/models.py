from django.db import models
from users.models import User

FIELD_TYPE = (
    ('turf', 'газон'),
    ('grass', 'трава'),
    ('indoor', 'в помещении'),
    ('sand', 'песок'),
    ('beach', 'пляж')
)


class Field(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    title = models.CharField(max_length=255)
    size = models.IntegerField()
    type = models.CharField(choices=FIELD_TYPE, max_length=20)
    service = models.JSONField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

    def __str__(self):
        return self.title


class Image(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/field_images')


class Game(models.Model):
    MATCH_TYPES = (
        ('friendly', 'товарищеский'),
        ('competitive', 'соревновательный'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    played_users = models.ManyToManyField(User)
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
    image = models.ImageField(upload_to='media/game_detail')

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return f'{self.title}'
