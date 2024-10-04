# Generated by Django 4.2.3 on 2024-07-22 11:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_alter_fanclub_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fanclub',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]