from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, ListView
from .models import Verse

# Create your views here.
#
class BookListView(ListView):
    model = Verse
    template_name = 'studies/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        books = Verse.objects.values('book').distinct()
        return books

class ChapterListView(ListView):
    model = Verse
    template_name = 'studies/chapter_list.html'
    context_object_name = 'chapters'

    def get_queryset(self):
        book = self.kwargs['book']
        chapters = Verse.objects.filter(book=book).values('chapter').distinct()
        return chapters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.kwargs['book']
        return context

class VerseListView(ListView):
    model = Verse
    template_name = 'studies/verse_list.html'

    def get_queryset(self):
        book = self.kwargs['book']
        chapter = self.kwargs['chapter']
        start = int(self.request.GET.get('start', 0))

        verses = Verse.objects.filter(book=book, chapter=chapter)[start:start+10]

        return verses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.kwargs['book']
        context['chapter'] = self.kwargs['chapter']
        start = int(self.request.GET.get('start', 0))
        context['start'] = start
        context['next_start'] = start + 10
        return context
