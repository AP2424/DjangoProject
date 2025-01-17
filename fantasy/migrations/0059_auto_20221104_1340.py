# Generated by Django 3.2.12 on 2022-11-04 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0058_club_place_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='champions_league_places',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='league',
            name='conference_league_places',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='league',
            name='europa_league_places',
            field=models.SmallIntegerField(default=0),
        ),
    ]
