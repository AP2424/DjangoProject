# Generated by Django 3.2.12 on 2022-08-18 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0036_team_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
