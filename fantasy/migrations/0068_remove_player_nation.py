# Generated by Django 3.2.12 on 2022-12-14 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0067_auto_20221214_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='nation',
        ),
    ]