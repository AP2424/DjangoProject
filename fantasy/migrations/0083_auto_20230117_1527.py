# Generated by Django 3.2.12 on 2023-01-17 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0082_auto_20230117_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='match',
            name='assisters',
        ),
        migrations.RemoveField(
            model_name='match',
            name='away_subs',
        ),
        migrations.RemoveField(
            model_name='match',
            name='booked',
        ),
        migrations.RemoveField(
            model_name='match',
            name='home_subs',
        ),
        migrations.RemoveField(
            model_name='match',
            name='sent_off',
        ),
        migrations.RemoveField(
            model_name='match',
            name='subbed_off',
        ),
        migrations.RemoveField(
            model_name='match',
            name='subbed_on',
        ),
        migrations.AddField(
            model_name='goal',
            name='assister',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assister', to='fantasy.player'),
        ),
        migrations.AddField(
            model_name='match',
            name='goals',
            field=models.ManyToManyField(default='', to='fantasy.Goal'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='scorer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='scorer', to='fantasy.player'),
        ),
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.SmallIntegerField(default=0)),
                ('type', models.CharField(default='', max_length=50)),
                ('player_off', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='player_off', to='fantasy.player')),
                ('player_on', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='player_on', to='fantasy.player')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='cards',
            field=models.ManyToManyField(default='', to='fantasy.Card'),
        ),
        migrations.AddField(
            model_name='match',
            name='subs',
            field=models.ManyToManyField(default='', to='fantasy.Substitution'),
        ),
    ]