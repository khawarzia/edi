# Generated by Django 2.2.3 on 2019-10-11 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileinfo', '0019_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
