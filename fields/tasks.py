from django.conf import settings

from main.celery import app
from .models import Reservation
from .fields_services import send_notification

from dateutil.relativedelta import relativedelta

import datetime


@app.task(name='delete_or_save_reservation')
def delete_or_save_reservation(reservation_id: object):
    reservation = Reservation.objects.get(id=reservation_id)
    user = reservation.user
    amount = reservation.field.price * reservation.duration

    if user.pocket.balance < amount:
        del reservation
        return {'status': 'DELETED', 'reason': 'NOT_ENOUGH_BALANCE'}
    else:
        owner = reservation.owner

        user.pocket.balance -= amount
        user.pocket.save(update_fields=['balance'])

        owner.pocket.balance += amount
        owner.pocket.save(update_fields=['pocket'])

        reservation.paid = True
        reservation.save(update_fields=['paid'])
        return {'status': 'SUCCESS', 'reason': 'PAID'}


@app.task(name='check_reservation')
def check_reservation_paid():
    date = datetime.datetime.now() + relativedelta(days=+2)
    queryset = Reservation.objects.filter(reservation_date__gte=date,
                                          reservation_date__lte=date+relativedelta(days=+3),
                                          status='not_checked')
    for query in queryset:
        print(query.status, query.id)
        user = query.user
        amount = query.field.price * query.duration

        if query.paid:
            return {'status': 'SUCCESS', 'reason': 'PAID'}

        elif user.pocket.balance < amount:
            send_notification(user.phone)
            delete_or_save_reservation.apply_async(args=(query.id,), countdown=43200)
            query.status = 'on_checking'
            query.save(update_fields=['status'])
            return {'status': 'SEND', 'reason': 'NOT_ENOUGH_BALANCE'}

        else:
            owner = query.field.owner

            user.pocket.balance -= amount
            user.pocket.save(update_fields=['balance'])

            owner.pocket.balance += amount
            owner.pocket.save(update_fields=['pocket'])

            query.paid = True
            query.save(update_fields=['paid'])
            return {'status': 'SUCCESS', 'reason': 'PAID'}


app.conf.beat_schedule = {
    'check-every-1-hours': {
        'task': 'check_reservation',
        'schedule': 3600.0,
    },
}
