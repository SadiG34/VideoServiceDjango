# Generated by Django 5.0.4 on 2024-04-20 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoservice', '0003_videotag_video_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_text',
            field=models.TextField(max_length=500, verbose_name='Текст комментария'),
        ),
    ]
