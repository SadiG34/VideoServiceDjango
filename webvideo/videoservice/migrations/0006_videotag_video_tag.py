# Generated by Django 5.0.4 on 2024-04-20 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoservice', '0005_remove_video_tag_delete_videotag'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.AddField(
            model_name='video',
            name='tag',
            field=models.ManyToManyField(to='videoservice.videotag', verbose_name='Тэг'),
        ),
    ]
