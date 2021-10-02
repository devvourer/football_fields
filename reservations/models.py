from django.db import models

from users.models import User
from fields.models import Field


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, related_name='reservations')

    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    duration = models.DecimalField(max_digits=2, decimal_places=1)

    paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        ordering = ()

    def __str__(self):
        return f'{self.user} : {self.field} : {self.reservation_date}'
