# Generated by Django 3.0.5 on 2020-05-19 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiccarapp', '0009_auto_20200520_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='endAddress',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ride',
            name='startAddress',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
