# Generated by Django 2.2.3 on 2019-09-20 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_auto_20190920_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name='infor',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
