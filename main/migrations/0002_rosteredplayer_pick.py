# Generated by Django 5.1.3 on 2024-11-27 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rosteredplayer',
            name='pick',
            field=models.IntegerField(default=0),
        ),
    ]
