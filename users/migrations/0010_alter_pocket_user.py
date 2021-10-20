# Generated by Django 3.2.7 on 2021-10-18 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pocket',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pocket', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
