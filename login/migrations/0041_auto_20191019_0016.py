# Generated by Django 2.2.3 on 2019-10-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0040_auto_20191016_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='infor',
            name='profile',
            field=models.IntegerField(default=2),
        ),
    ]
