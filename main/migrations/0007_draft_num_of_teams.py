# Generated by Django 5.1.3 on 2024-12-04 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_team_user_draftplayer_delete_rosteredplayer'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='num_of_teams',
            field=models.IntegerField(default=0),
        ),
    ]
