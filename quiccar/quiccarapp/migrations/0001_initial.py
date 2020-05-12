# Generated by Django 3.0.5 on 2020-05-12 18:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startX', models.DecimalField(decimal_places=6, max_digits=9)),
                ('startY', models.DecimalField(decimal_places=6, max_digits=9)),
                ('endX', models.DecimalField(decimal_places=6, max_digits=9)),
                ('endY', models.DecimalField(decimal_places=6, max_digits=9)),
                ('startHash', models.CharField(db_index=True, max_length=12, null=True)),
                ('endHash', models.CharField(db_index=True, max_length=12, null=True)),
                ('startAddress', models.CharField(max_length=100)),
                ('endAddress', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('capacity', models.IntegerField()),
                ('isActive', models.BooleanField()),
                ('timeInserted', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]{10}$', 'Invalid phone number')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
