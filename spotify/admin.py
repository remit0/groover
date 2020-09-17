from django.contrib import admin

from .models import SpotifyToken, Artist, Album

admin.site.register(SpotifyToken)
admin.site.register(Artist)
admin.site.register(Album)
