"""
Django management command to populate the database with sample books.
Usage: python manage.py populate_books
"""

from django.core.management.base import BaseCommand
from api.models import Book


class Command(BaseCommand):
    help = 'Populate the database with sample books for testing the API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing books before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing books...')
            Book.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing books cleared.'))

        # Sample books data
        sample_books = [
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
            {'title': '1984', 'author': 'George Orwell'},
            {'title': 'Pride and Prejudice', 'author': 'Jane Austen'},
            {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger'},
            {'title': 'Lord of the Flies', 'author': 'William Golding'},
            {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien'},
            {'title': 'Harry Potter and the Philosopher\'s Stone', 'author': 'J.K. Rowling'},
            {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien'},
            {'title': 'Fahrenheit 451', 'author': 'Ray Bradbury'},
            {'title': 'Brave New World', 'author': 'Aldous Huxley'},
            {'title': 'The Chronicles of Narnia', 'author': 'C.S. Lewis'},
            {'title': 'Dune', 'author': 'Frank Herbert'},
            {'title': 'The Hitchhiker\'s Guide to the Galaxy', 'author': 'Douglas Adams'},
            {'title': 'Foundation', 'author': 'Isaac Asimov'},
        ]

        created_count = 0
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                author=book_data['author']
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created: {book.title} by {book.author}')
            else:
                self.stdout.write(f'Already exists: {book.title} by {book.author}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with {created_count} new books. '
                f'Total books in database: {Book.objects.count()}'
            )
        )
