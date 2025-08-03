from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book
from .models import Library

# Create your views here.

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    This view should render a simple text list of book titles and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
# Utilize Django's ListView or DetailView to structure this class-based view
class LibraryDetailView(DetailView):
    """
    Create a class-based view in relationship_app/views.py that displays details for a specific library,
    listing all books available in that library.
    Utilize Django's ListView or DetailView to structure this class-based view.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
