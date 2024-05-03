from django.shortcuts import render, reverse
from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from hitcount.views import HitCountDetailView
from django.views import View
from django.db.models import Q, Count

from profiles.models import Profile


class home_view(ListView):
    model = Video
    template_name = 'videoservice/home.html'
    order_by = 'views'

class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'file', 'thumbnail', 'tag' ]
    template_name = 'videoservice/create_video.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return  reverse('video-detail', kwargs={'pk': self.object.pk})

class DetailVideo(HitCountDetailView, View):
    model = Video
    template_name = 'videoservice/detail_video.html'
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        profile = Profile

        data = super().get_context_data(**kwargs)
        video = self.get_object()
        tags = Video.objects.filter(tag__in=video.tag.all())[:15]

        likes_connected = get_object_or_404(Video, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        if self.request.user.is_authenticated:
            user_is_subscribed = Subscription.objects.filter(subscriber=self.request.user,
                                                             subscribed_to=video.user).exists()
            video = Video.objects.get(id=video.id)
            number_of_subscribers = Subscription.objects.filter(subscribed_to=video.user).aggregate(subscribers_count=Count('id'))[
                'subscribers_count']
            data['number_of_subscribers'] = number_of_subscribers
        else:
            data['number_of_subscribers'] = Subscription.objects.filter(subscribed_to=video.user).aggregate(subscribers_count=Count('id'))[
                'subscribers_count']

            user_is_subscribed = False

        form = CommentForm()
        comments = Comments.objects.filter(video=video).order_by('-timestamp')
        data['user_is_subscribed'] = user_is_subscribed
        data['comments'] = comments
        data['profile'] = profile
        data['form'] = form
        data['tags'] = tags

        return data

    def post(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comments(
                user=self.request.user,
                comment_text=form.cleaned_data['comment'],
                video=video
            )
            comment.save()

            # Очистить поле комментария в форме
            form = CommentForm()

        comments = Comments.objects.filter(video=video).order_by('-timestamp')
        tags = Video.objects.filter(tag__in=video.tag.all())[:15]

        context = {
            'object': video,
            'comments': comments,
            'form': form,
            'tags': tags,
        }


        return render(request, 'videoservice/detail_video.html', context)


def VideoLike(request, pk):
    video = get_object_or_404(Video, id=request.POST.get('video_id'))
    if video.likes.filter(id=request.user.id).exists():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)

    return HttpResponseRedirect(reverse('video-detail', args=[str(pk)]))
class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'tag', 'thumbnail', 'file']
    template_name = 'videoservice/create_video.html'


    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.user
class DeleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'videoservice/delete_video.html'

    def get_success_url(self):
        return reverse('home')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.user


class VideoTagList(View):
    def get(self, request, pk, *args, **kwargs):
        tag = VideoTag.objects.get(pk=int(pk))
        videos = Video.objects.filter(tag=pk).order_by('-date_posted')
        context = {
            'tag': tag,
            'videos': videos
        }

        return render(request, 'videoservice/video_tag.html', context)


class SearchVideo(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        query_list = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username__icontains=query)
        )

        context = {
            'query_list': query_list,
        }

        return render(request, 'videoservice/search.html', context)


class SubscribeUser(View):
    def post(self, request, pk, *args, **kwargs):
        subscribed_to = get_object_or_404(User, pk=pk)
        subscriber = request.user

        if subscriber != subscribed_to:
            subscription, created = Subscription.objects.get_or_create(subscriber=subscriber,
                                                                       subscribed_to=subscribed_to)
            if created:
                return JsonResponse({'result': 'subscribed'})
            else:
                return JsonResponse({'result': 'already_subscribed'})
        else:
            return JsonResponse({'result': 'self_subscribe_error'})


class UnsubscribeUser(View):
    def post(self, request, pk, *args, **kwargs):
        subscribed_to = get_object_or_404(User, pk=pk)
        subscriber = request.user
        Subscription.objects.filter(subscriber=subscriber, subscribed_to=subscribed_to).delete()
        return JsonResponse({'result': 'unsubscribed'})
