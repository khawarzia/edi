# Generated by Django 2.2 on 2020-03-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0069_auto_20200316_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=13),
        ),
    ]