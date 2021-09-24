from django.db import models

from users.models import User

from uuid import uuid4


class PaymentOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_order_id = models.UUIDField(default=uuid4, verbose_name='Идентификатор платежа')

    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Сумма платежа')
    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True,verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновленно')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежы'

    def __str__(self):
        return f'{self.user} : {self.amount} : {self.created}'
