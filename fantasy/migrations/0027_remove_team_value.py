# Generated by Django 3.2.12 on 2022-07-31 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0026_alter_team_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='value',
        ),
    ]
