# Generated by Django 2.2.3 on 2020-01-05 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0056_auto_20200105_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=3),
        ),
    ]
