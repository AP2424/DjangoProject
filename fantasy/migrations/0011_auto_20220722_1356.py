# Generated by Django 3.2.12 on 2022-07-22 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0010_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='players',
        ),
        migrations.AddField(
            model_name='team',
            name='players',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fantasy.player'),
        ),
    ]