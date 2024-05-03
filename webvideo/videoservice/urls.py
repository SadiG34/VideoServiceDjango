from django.urls import path

from .views import *

urlpatterns = [
    path('create/', CreateVideo.as_view(), name='video-create'),
    path('<int:pk>/', DetailVideo.as_view(), name='video-detail'),
    path('<int:pk>/update', UpdateVideo.as_view(), name='video-update'),
    path('<int:pk>/delete', DeleteVideo.as_view(), name='video-delete'),
    path('video-like/<int:pk>', VideoLike, name="video_like"),
    path('tag/<int:pk>', VideoTagList.as_view(), name='tag-list'),
    path('search/', SearchVideo.as_view(), name='video-search'),
    path('subscribe/<int:pk>/', SubscribeUser.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>/', UnsubscribeUser.as_view(), name='unsubscribe'),
]