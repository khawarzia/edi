# Generated by Django 2.2.3 on 2019-10-26 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0045_auto_20191026_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=20),
        ),
    ]
