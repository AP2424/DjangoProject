# Generated by Django 3.2.12 on 2022-12-30 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0074_team_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Minute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='assisters',
            field=models.ManyToManyField(default='', related_name='assisters', to='fantasy.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='booked',
            field=models.ManyToManyField(default='', related_name='booked', to='fantasy.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='scorers',
            field=models.ManyToManyField(default='', related_name='scorers', to='fantasy.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='sent_off',
            field=models.ManyToManyField(default='', related_name='sent_off', to='fantasy.Player'),
        ),
    ]
