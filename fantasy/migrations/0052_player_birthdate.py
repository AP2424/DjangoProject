# Generated by Django 3.2.12 on 2022-10-07 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0051_player_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='birthdate',
            field=models.CharField(default='', max_length=50),
        ),
    ]