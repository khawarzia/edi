# Generated by Django 2.2.3 on 2019-12-01 18:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileinfo', '0033_auto_20191201_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='reluser',
            field=models.ManyToManyField(related_name='reluser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='sel',
            field=models.CharField(blank=True, choices=[('post', 'post'), ('comment', 'comment'), ('follow', 'follow')], max_length=20),
        ),
    ]