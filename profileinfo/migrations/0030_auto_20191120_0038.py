# Generated by Django 2.2.3 on 2019-11-19 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileinfo', '0029_auto_20191111_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='relcom',
            field=models.ManyToManyField(to='profileinfo.comment'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='relcomchild',
            field=models.ManyToManyField(to='profileinfo.comment_child'),
        ),
    ]