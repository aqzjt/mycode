# Generated by Django 2.1.3 on 2018-12-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m3u8', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ts',
            name='ts',
            field=models.TimeField(),
        ),
    ]
