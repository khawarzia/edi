# Generated by Django 2.2.3 on 2019-10-09 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0032_auto_20191009_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='infor',
            name='profile',
            field=models.IntegerField(default=2),
        ),
    ]
