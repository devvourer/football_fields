# Generated by Django 3.2.7 on 2021-10-11 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0003_alter_field_services'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='services',
        ),
        migrations.AddField(
            model_name='field',
            name='services',
            field=models.CharField(choices=[('water', 'вода'), ('cloakroom', 'раздевалка'), ('shower', 'душ')], default=None, max_length=255),
        ),
    ]
