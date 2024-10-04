# Generated by Django 4.2.3 on 2024-06-22 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0119_stadium_clubteam_city_nationalteam_confederation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='id',
        ),
        migrations.RemoveField(
            model_name='league',
            name='image',
        ),
        migrations.RemoveField(
            model_name='league',
            name='matchdays_url',
        ),
        migrations.RemoveField(
            model_name='league',
            name='name',
        ),
        migrations.RemoveField(
            model_name='league',
            name='url',
        ),
        migrations.RemoveField(
            model_name='match',
            name='league',
        ),
        migrations.AddField(
            model_name='league',
            name='competition_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fantasy.competition'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='competition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fantasy.competition'),
        ),
    ]