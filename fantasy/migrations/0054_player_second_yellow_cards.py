# Generated by Django 3.2.12 on 2022-10-14 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0053_auto_20221014_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='second_yellow_cards',
            field=models.SmallIntegerField(default=0),
        ),
    ]
