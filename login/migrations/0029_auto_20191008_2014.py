# Generated by Django 2.2.3 on 2019-10-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0028_auto_20191008_0008'),
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
