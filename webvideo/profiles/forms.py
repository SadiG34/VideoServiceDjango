from django import forms
from .models import Profile

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, label='Имя')
    location = forms.CharField(max_length=80, label='Страна')
    image = forms.ImageField(required=False, label='Фото профиля')

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        if not image:
            cleaned_data['image'] = 'uploads/profile_pics/default.jpg'
        return cleaned_data

    def signup(self, request, user):
        user.save()
        profile = Profile()
        profile.user = user
        profile.name = self.cleaned_data['name']
        profile.location = self.cleaned_data['location']
        profile.image = self.cleaned_data['image']
        profile.save()