# Generated by Django 4.1.5 on 2023-06-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0110_pollchoice_choiceid'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='number_of_queries',
            field=models.BigIntegerField(default=0),
        ),
    ]