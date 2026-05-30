import json
import urllib.parse
import urllib.request
from django.core.management.base import BaseCommand
from studies.models import Verse

BOOKS = [
    'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
    'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
    '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
    'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs',
    'Ecclesiastes', 'Song Of Solomon', 'Isaiah', 'Jeremiah',
    'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
    'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
    'Haggai', 'Zechariah', 'Malachi',
    'Matthew', 'Mark', 'Luke', 'John', 'Acts',
    'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
    'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
    '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
    'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
    'Jude', 'Revelation',
]

BASE_URL = 'https://cdn.jsdelivr.net/gh/aruljohn/Bible-niv'
TRANSLATION = 'NIV'


class Command(BaseCommand):
    help = 'Downloads the NIV Bible and loads all verses into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing NIV verses before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = Verse.objects.filter(translation=TRANSLATION).delete()
            self.stdout.write(f'Cleared {deleted} existing NIV verses.')

        verses_to_create = []
        total_books = 0

        for book_name in BOOKS:
            encoded = urllib.parse.quote(book_name)
            url = f'{BASE_URL}/{encoded}.json'
            self.stdout.write(f'Downloading {book_name}...')

            try:
                with urllib.request.urlopen(url, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
            except Exception as e:
                self.stderr.write(f'  Failed: {e}')
                continue

            for chapter in data.get('chapters', []):
                chapter_num = int(chapter['chapter'])
                for verse in chapter.get('verses', []):
                    verse_num = int(verse['verse'])
                    verses_to_create.append(Verse(
                        translation=TRANSLATION,
                        book=data['book'],
                        chapter=chapter_num,
                        verse_start=verse_num,
                        text=verse['text'],
                    ))

            total_books += 1

        self.stdout.write(f'\nInserting {len(verses_to_create)} verses...')
        Verse.objects.bulk_create(verses_to_create, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f'Done! {total_books} books, {len(verses_to_create)} verses loaded.'
        ))


