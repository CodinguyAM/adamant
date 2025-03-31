# Generated by Django 5.0.6 on 2025-03-24 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_user_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_tli',
            field=models.CharField(default='ZZZ', max_length=3),
        ),
        migrations.AlterField(
            model_name='game',
            name='code',
            field=models.CharField(max_length=9, unique=True),
        ),
    ]
