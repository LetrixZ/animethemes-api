# Generated by Django 3.1 on 2020-08-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_remove_anime_themes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='mal_id',
            field=models.IntegerField(unique=True),
        ),
    ]