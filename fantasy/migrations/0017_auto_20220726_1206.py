# Generated by Django 3.2.12 on 2022-07-26 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0016_alter_club_league'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='club',
        ),
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
