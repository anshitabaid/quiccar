# Generated by Django 3.0.5 on 2020-05-28 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiccarapp', '0010_auto_20200520_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='isActive',
            field=models.BooleanField(blank=True),
        ),
    ]
