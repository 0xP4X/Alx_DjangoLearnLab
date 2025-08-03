from django.contrib import admin
from .models import Book

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters for these fields in the admin sidebar
    list_filter = ('author', 'publication_year')

    # Enable search functionality for these fields
    search_fields = ('title', 'author')

    # Add ordering
    ordering = ('title',)

    # Number of items per page
    list_per_page = 20

    # Add date hierarchy (if you had date fields)
    # date_hierarchy = 'publication_date'

    # Fields to display in the edit form
    fields = ('title', 'author', 'publication_year')

    # Make certain fields read-only (example)
    # readonly_fields = ('publication_year',)

# Register the Book model with the custom BookAdmin configuration
admin.site.register(Book, BookAdmin)
