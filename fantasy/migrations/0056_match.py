# Generated by Django 3.2.12 on 2022-10-24 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0055_remove_league_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_goals', models.SmallIntegerField(default=0)),
                ('away_goals', models.SmallIntegerField(default=0)),
                ('away_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away', to='fantasy.club')),
                ('home_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home', to='fantasy.club')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fantasy.league')),
            ],
        ),
    ]