# Generated by Django 2.2.3 on 2019-08-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20190823_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='infor',
            name='paypal_url',
            field=models.URLField(null=True),
        ),
    ]
