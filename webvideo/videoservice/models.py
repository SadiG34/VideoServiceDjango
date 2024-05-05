from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from profiles.models import Profile

User = get_user_model()

class VideoTag(models.Model):
    title = models.CharField(max_length=32, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Playlist(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название плейлиста')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'
class Video(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название видео')
    description = models.TextField(max_length=500, verbose_name='Описание видео')
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0, verbose_name='Пользователь')
    thumbnail = models.FileField(upload_to='uploads/thumbnails',
                                 validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name='Заставка')
    date_posted = models.DateTimeField(default=timezone.now)
    file = models.FileField(
        upload_to='uploads/video_files/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])], verbose_name='Видеофайл')
    tag = models.ManyToManyField(VideoTag, verbose_name='Тэг')
    views = models.IntegerField(verbose_name='Количество просмотров', default=0)
    likes = models.ManyToManyField(User, related_name='Лайки')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
#добавление тегов, плейлисты (смотреть позже и т.д),


class Comments(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    comment_text = models.TextField(max_length=500, verbose_name='Текст комментария')
    timestamp = models.DateTimeField(verbose_name='Временная метка комментария', auto_now_add=True)

    def __str__(self):
        return f'Пользователь: {self.user} | Создано:  {self.timestamp.strftime("%b %d %Y %I:%M %p")}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber', verbose_name='Subscriber')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribed_to', verbose_name='Subscribed To')

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')