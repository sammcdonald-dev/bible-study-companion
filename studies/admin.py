from django.contrib import admin
from .models import Verse, Collection, ProgressEntry
# Register your models here.

@admin.register(Verse)
class AdminVerse(admin.ModelAdmin):
    list_display = ('__str__', 'book', 'chapter', 'translation')
    search_fields = ('book', 'text')

@admin.register(Collection)
class AdminCollection(admin.ModelAdmin):
    list_display = ('title', 'user', 'verse_count', 'created_at')
    filter_horizontal = ('verses',)

@admin.register(ProgressEntry)
class AdminProgressEntry(admin.ModelAdmin):
    list_display = ('user', 'verse', 'read_at')
    list_filter = ('read_at', 'user')
