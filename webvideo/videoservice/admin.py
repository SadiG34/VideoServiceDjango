from django.contrib import admin
from .models import *

admin.site.register(Video)
admin.site.register(Comments)
admin.site.register(Playlist)
admin.site.register(VideoTag)

