# Generated by Django 3.2.12 on 2022-12-14 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0068_remove_player_nation'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='nation',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='fantasy.nation'),
        ),
    ]