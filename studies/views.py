from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from django.views.generic.edit import CreateView

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
        context['next_start'] = start + 8
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
