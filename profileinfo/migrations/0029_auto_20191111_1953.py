# Generated by Django 2.2.3 on 2019-11-11 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileinfo', '0028_auto_20191111_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
