# Generated by Django 3.2.12 on 2023-01-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0078_auto_20230101_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='away_squad',
            field=models.ManyToManyField(default='', related_name='away_squad', to='fantasy.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='home_squad',
            field=models.ManyToManyField(default='', related_name='home_squad', to='fantasy.Player'),
        ),
    ]
