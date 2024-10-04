# Generated by Django 3.2.12 on 2023-01-17 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0084_auto_20230117_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='away_subs',
            field=models.ManyToManyField(default='', related_name='away_subs', to='fantasy.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='home_subs',
            field=models.ManyToManyField(default='', related_name='home_subs', to='fantasy.Player'),
        ),
    ]