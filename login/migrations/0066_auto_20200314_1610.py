# Generated by Django 2.2 on 2020-03-14 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0065_auto_20200117_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='infor',
            name='profile',
            field=models.IntegerField(default=2),
        ),
    ]
