from django.contrib import admin
from .models import User, Pocket, Profile, Owner
# Register your models here.

admin.site.register(User)
admin.site.register(Pocket)
admin.site.register(Profile)
admin.site.register(Owner)