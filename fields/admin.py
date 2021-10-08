from django.contrib import admin
from .models import Field, Game, Service, FavouriteField, Reservation

admin.site.register(Field)
admin.site.register(Game)
admin.site.register(Service)
admin.site.register(FavouriteField)
admin.site.register(Reservation)
