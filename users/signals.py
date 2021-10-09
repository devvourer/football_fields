from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    try:
        if created:
            Profile.objects.create(user=instance)
            print("Profile created !!!")
    except Exception:
        print(" Profile wasn't created !!!")

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):

    if created == False:
        instance.profile.save()
        print('Profile update')

