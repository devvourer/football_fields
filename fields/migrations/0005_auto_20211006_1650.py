# Generated by Django 3.2.7 on 2021-10-06 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0004_auto_20211001_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('water', 'вода'), ('cloakroom', 'раздевалка'), ('shower', 'душ')], max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='field',
            name='service',
        ),
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.CharField(choices=[('turf', 'газон'), ('grass', 'трава'), ('indoor', 'крытый'), ('sand', 'песок'), ('beach', 'пляж')], max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='field_type',
            field=models.CharField(choices=[('turf', 'газон'), ('grass', 'трава'), ('indoor', 'крытый'), ('sand', 'песок'), ('beach', 'пляж')], max_length=100),
        ),
        migrations.AddField(
            model_name='field',
            name='services',
            field=models.ManyToManyField(to='fields.Service'),
        ),
    ]
