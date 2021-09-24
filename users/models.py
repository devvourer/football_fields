from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The number must be set')

        phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):

    username = None
    phone = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['password', ]

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone


class Profile(models.Model):
    FOOT = (
        ('right', 'right'),
        ('left', 'left')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to='media/avatars')
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    foot = models.CharField(max_length=5, choices=FOOT, default='right')
    favourite_club = models.CharField(max_length=100, null=True, blank=True)
    jersey_number = models.IntegerField(null=True, blank=True)
    position_primary = models.CharField(max_length=50)
    position_secondary = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user} : {self.name}'


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card = models.CharField(max_length=16)


class Pocket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    balance = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'

    def __str__(self):
        return f'{self.user}: {self.balance}'





