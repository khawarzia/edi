# Generated by Django 2.2.3 on 2019-10-11 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0038_auto_20191012_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=13),
        ),
    ]
