# Generated by Django 2.2.3 on 2019-10-11 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileinfo', '0017_auto_20191011_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='linked_checked',
            field=models.BooleanField(default=False),
        ),
    ]
