# Generated by Django 3.2.12 on 2022-12-14 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0064_nation'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='nation',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='fantasy.nation'),
        ),
    ]
