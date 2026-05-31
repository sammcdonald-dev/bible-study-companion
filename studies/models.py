from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Verse(models.Model):
    translation = models.CharField(max_length=20, default="ESV")
    book = models.CharField(max_length=50)
    chapter = models.PositiveIntegerField()
    verse_start = models.PositiveIntegerField()
    # verse_end = models.PositiveIntegerField() passage will now be verse by verse

    text = models.TextField()

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

    verses = models.ManyToManyField(
        Verse,
        related_name='collections',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def verse_count(self):
        return self.verses.count()

class ProgressEntry(models.Model):
    class Meta:
        ordering = ['-read_at']
        unique_together = ('user', 'verse')
        # orders by last read
        # and user and passage
        # unique to each other

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress_entries'
    )
    verse = models.ForeignKey(
        Verse,
        on_delete=models.CASCADE,
        related_name="progress_entries",
        blank=True,
        default='John 3:16'
    )
    read_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} read {self.verse}"
