# Generated by Django 2.2 on 2020-03-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0068_auto_20200315_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=16),
        ),
    ]
