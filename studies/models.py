from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Passage(models.Model):
    translation = models.CharField(max_length=20, default="ESV")
    book = models.CharField(max_length=50)
    chapter = models.PositiveIntegerField()
    verse_start = models.PositiveIntegerField()
    verse_end = models.PositiveIntegerField()

    text = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.book} {self.chapter}:{self.verse_start}"


class Collection(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    passages = models.ManyToManyField(
        Passage,
        related_name='collections',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def passage_count(self):
        return self.passages.count()

class ProgressEntry(models.Model):
    class Meta:
        ordering = ['-read_at']
        unique_together = ('user', 'passage')
        # orders by last read
        # and user and passage
        # unique to each other

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress_entries'
    )
    passage = models.ForeignKey(
        Passage,
        on_delete=models.CASCADE,
        related_name="progress_entries",
    )
    read_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} read {self.passage}"
