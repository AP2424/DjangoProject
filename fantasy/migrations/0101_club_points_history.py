# Generated by Django 4.1.5 on 2023-02-05 11:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0100_remove_match_club_remove_match_stage_delete_clubscup'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='points_history',
            field=models.CharField(default='', max_length=100, validators=[django.core.validators.int_list_validator]),
        ),
    ]
