# Generated by Django 3.2.12 on 2022-07-31 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0023_team_players'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='selected',
        ),
        migrations.RemoveField(
            model_name='team',
            name='created',
        ),
    ]