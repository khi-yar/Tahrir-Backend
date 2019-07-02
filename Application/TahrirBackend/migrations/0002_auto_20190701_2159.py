# Generated by Django 2.2.2 on 2019-07-01 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TahrirBackend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='englishword',
            name='word',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='fatoentranslation',
            name='submitter_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='persianword',
            name='word',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]