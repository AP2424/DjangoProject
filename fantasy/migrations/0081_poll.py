# Generated by Django 3.2.12 on 2023-01-09 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0080_auto_20230101_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('type', models.CharField(choices=[(1, 'poll'), (2, 'quiz')], max_length=10)),
            ],
        ),
    ]