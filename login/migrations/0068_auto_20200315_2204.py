# Generated by Django 2.2 on 2020-03-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0067_auto_20200314_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='infor',
            name='profile',
            field=models.IntegerField(default=1),
        ),
    ]
