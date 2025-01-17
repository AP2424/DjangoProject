# Generated by Django 4.1.5 on 2023-01-25 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0090_internationalcup'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubCup',
            fields=[
                ('internationalcup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fantasy.internationalcup')),
                ('clubs', models.ManyToManyField(to='fantasy.club')),
            ],
            bases=('fantasy.internationalcup',),
        ),
    ]
