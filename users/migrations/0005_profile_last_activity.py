# Generated by Django 4.2.3 on 2024-08-07 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220721_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]