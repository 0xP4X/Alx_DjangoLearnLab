from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    Provides a user-friendly interface for managing books.
    """
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author')
    ordering = ('title',)
