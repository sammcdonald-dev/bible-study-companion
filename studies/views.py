from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect

from studies.forms import UserSignUpForm
from .models import Verse, ProgressEntry
from django.urls import reverse_lazy

# Create your views here.
#
#
class HomeView(View):
    template_name = 'studies/home.html'

    def get(self, request):
        user = request.user
        last_verse_read = None
        reading_progress = 0.00

        if request.user.is_authenticated:
            last_verse_read = ProgressEntry.objects.filter(user=user).first()
            verses_read = ProgressEntry.objects.filter(user=user).count()
            total_verses = Verse.objects.count()
            if total_verses:
                reading_progress = (verses_read / total_verses) * 100

        context = {
            'reading_progress': reading_progress,
            'last_verse_read': last_verse_read
        }
        return render(request, self.template_name, context)

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

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.book = self.kwargs['book']
        self.chapter = self.kwargs['chapter']
        self.start = int(request.GET.get('start', 0))

        self.verses_per_chapter = Verse.objects.filter(
            book=self.book,
            chapter=self.chapter
        ).count()

        self.chapters_per_book = Verse.objects.filter(
            book=self.book
        ).values('chapter').count()

    def get(self, request, *args, **kwargs):
        # save a progress entry on view
        if self.start >= self.verses_per_chapter:
            return redirect('verses-section', self.book, self.chapter + 1)

        if request.user.is_authenticated:
            for verse in self.get_queryset():
                entry, created = ProgressEntry.objects.get_or_create(
                    user=request.user,
                    verse=verse
                )
        # Otherwuise list View handles it normally
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        verses = Verse.objects.filter(
            book=self.book,
            chapter=self.chapter
        )[self.start:self.start+8]
        return verses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        context['chapter'] = self.chapter
        context['start'] = self.start
        context['next_start'] = self.start + 8

        context['verses_per_chapter'] = self.verses_per_chapter
        context['chapters_per_book'] = self.chapters_per_book
        context['has_more_verses'] = self.verses_per_chapter > self.start
        context['next_chapter'] = self.chapter + 1

        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'studies/profile.html'


class SignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = 'studies/signup.html'
    success_url = reverse_lazy('login')

# reverse() runs immediately when the class is defined —
# which happens at import time before Django has fully
# loaded all the URLs. So it crashes.
# reverse_lazy() waits until the URL
# is actually needed before resolving it —
# by which point Django is fully loaded
# and knows about all your URL names.
