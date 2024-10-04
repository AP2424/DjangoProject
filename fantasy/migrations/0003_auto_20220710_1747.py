# Generated by Django 3.2.12 on 2022-07-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0002_auto_20220703_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='player_pics'),
        ),
        migrations.AddField(
            model_name='player',
            name='nation',
            field=models.CharField(default='n/a', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='number',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='age',
            field=models.SmallIntegerField(),
        ),
    ]