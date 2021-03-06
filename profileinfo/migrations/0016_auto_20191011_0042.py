# Generated by Django 2.2.3 on 2019-10-10 19:42

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileinfo', '0015_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='relpost',
        ),
        migrations.AddField(
            model_name='comment',
            name='relpost',
            field=models.ManyToManyField(null=True, to='profileinfo.post'),
        ),
        migrations.RemoveField(
            model_name='comment_child',
            name='relcomment',
        ),
        migrations.AddField(
            model_name='comment_child',
            name='relcomment',
            field=models.ManyToManyField(null=True, to='profileinfo.comment'),
        ),
        migrations.RemoveField(
            model_name='comment_child',
            name='relpost',
        ),
        migrations.AddField(
            model_name='comment_child',
            name='relpost',
            field=models.ManyToManyField(null=True, to='profileinfo.post'),
        ),
        migrations.RemoveField(
            model_name='message',
            name='reciever',
        ),
        migrations.AddField(
            model_name='message',
            name='reciever',
            field=models.ManyToManyField(null=True, related_name='reciever', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=ckeditor.fields.RichTextField(unique=True),
        ),
    ]
