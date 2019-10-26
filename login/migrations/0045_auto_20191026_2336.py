# Generated by Django 2.2.3 on 2019-10-26 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0044_auto_20191026_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infor',
            name='choice',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='infor',
            name='cover',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='infor',
            name='cover_img',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='infor',
            name='passwordkey',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='infor',
            name='paypal_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='infor',
            name='profile',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='infor',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='infor',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='infor',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='privacy_policy_and_terms_of_service',
            name='privacy_policy',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='privacy_policy_and_terms_of_service',
            name='terms_of_service',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='temppic',
            name='file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='userpreferance',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
