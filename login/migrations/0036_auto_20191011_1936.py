# Generated by Django 2.2.3 on 2019-10-11 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0035_auto_20191011_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='infor',
            name='profile',
            field=models.IntegerField(default=1),
        ),
    ]
