# Generated by Django 2.2 on 2020-03-16 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileinfo', '0046_auto_20200316_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postgallery',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postgallery',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
