# Generated by Django 3.2.12 on 2022-12-31 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0075_auto_20221230_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='subbed_off',
            field=models.ManyToManyField(default='', related_name='subbed_off', to='fantasy.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='subbed_on',
            field=models.ManyToManyField(default='', related_name='subbed_on', to='fantasy.Player'),
        ),
    ]