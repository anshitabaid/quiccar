# Generated by Django 3.0.5 on 2020-04-14 13:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]{10}$', 'Invalid phone number')])),
                ('startX', models.DecimalField(decimal_places=6, max_digits=9)),
                ('startY', models.DecimalField(decimal_places=6, max_digits=9)),
                ('endX', models.DecimalField(decimal_places=6, max_digits=9)),
                ('endY', models.DecimalField(decimal_places=6, max_digits=9)),
                ('startHash', models.CharField(max_length=12)),
                ('endHash', models.CharField(max_length=12)),
                ('startAddress', models.CharField(max_length=100)),
                ('endAddress', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('capacity', models.IntegerField()),
                ('isActive', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('number', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{10}$', 'Invalid phone number')])),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('firstname', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+$', 'Only letters alllowed')])),
                ('lastname', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+$', 'Only letters alllowed')])),
            ],
        ),
    ]