# Generated by Django 3.2.12 on 2022-12-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0072_remove_nation_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='logo',
        ),
        migrations.AddField(
            model_name='club',
            name='logo_url',
            field=models.URLField(default=''),
        ),
    ]