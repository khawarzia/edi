# Generated by Django 2.2 on 2020-03-14 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0066_auto_20200314_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=6),
        ),
    ]