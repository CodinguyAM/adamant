# Generated by Django 5.0.6 on 2025-06-28 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_game_made_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='background_highlight_color',
            field=models.CharField(default='#AAAAAA', max_length=7),
        ),
    ]
