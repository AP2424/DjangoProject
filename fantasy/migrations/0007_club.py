# Generated by Django 3.2.12 on 2022-07-20 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0006_alter_player_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]