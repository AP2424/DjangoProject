# Generated by Django 4.1.5 on 2023-01-28 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0097_clubscup_image_clubscup_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaguematch',
            name='league',
        ),
        migrations.RemoveField(
            model_name='leaguematch',
            name='match_ptr',
        ),
        migrations.AddField(
            model_name='match',
            name='clubcup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fantasy.clubscup'),
        ),
        migrations.AddField(
            model_name='match',
            name='leaguekey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fantasy.league'),
        ),
        migrations.AddField(
            model_name='match',
            name='matchdaynum',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='stagenum',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='CupMatch',
        ),
        migrations.DeleteModel(
            name='LeagueMatch',
        ),
    ]
