# Generated by Django 3.0.5 on 2020-05-15 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiccarapp', '0005_auto_20200515_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordreset',
            name='id',
        ),
        migrations.AlterField(
            model_name='passwordreset',
            name='username',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
    ]
