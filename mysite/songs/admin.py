from django.contrib import admin
from songs.models import Producer, Artist, Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'genre', 'year')
    list_filter = ('year',)
    search_fields = ('title', 'artist__name')
    ordering = ('-year',)


admin.site.register(Producer)
admin.site.register(Artist)
admin.site.register(Song, SongAdmin)