from django.contrib import admin
from .models import Passage, Collection, ProgressEntry
# Register your models here.

@admin.register(Passage)
class AdminPassage(admin.ModelAdmin):
    list_display = ('__str__', 'book', 'chapter', 'translation')
    search_fields = ('book', 'text')

@admin.register(Collection)
class AdminCollection(admin.ModelAdmin):
    list_display = ('title', 'user', 'passage_count', 'created_at')
    filter_horizontal = ('passages',)

@admin.register(ProgressEntry)
class AdminProgressEntry(admin.ModelAdmin):
    list_display = ('user', 'passage', 'read_at')
    list_filter = ('read_at', 'user')
