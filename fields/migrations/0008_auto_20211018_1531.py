# Generated by Django 3.2.7 on 2021-10-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0007_auto_20211008_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='is_active',
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('not_checked', 'не проверен'), ('on_checking', 'на проверке'), ('checked', 'проверен')], default='not_checked', max_length=12),
        ),
    ]