# Generated by Django 3.2.12 on 2022-07-24 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0015_club_league'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fantasy.league'),
        ),
    ]