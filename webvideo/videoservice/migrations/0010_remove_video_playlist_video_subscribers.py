# Generated by Django 5.0.4 on 2024-04-25 18:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoservice', '0009_delete_subscription'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='playlist',
        ),
        migrations.AddField(
            model_name='video',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='video_subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
