from django.shortcuts import render
from django.http import JsonResponse
from .models import Book


def api_home(request):
    """
    Basic API home view for testing the setup.
    This will be replaced with proper DRF views once Django REST Framework is integrated.
    """
    # Get basic statistics
    book_count = Book.objects.count()

    # Return basic API information
    data = {
        'message': 'Welcome to the Django REST Framework API Project',
        'status': 'Setup Complete',
        'django_version': '5.2.4',
        'api_app': 'Active',
        'book_count': book_count,
        'next_steps': [
            'Install Django REST Framework: pip install djangorestframework',
            'Uncomment rest_framework in INSTALLED_APPS',
            'Create serializers for the Book model',
            'Implement DRF ViewSets and API endpoints'
        ],
        'endpoints': {
            'current': {
                'api_home': '/api/',
                'admin': '/admin/',
            },
            'future_with_drf': {
                'books_list': '/api/books/',
                'book_detail': '/api/books/{id}/',
                'api_root': '/api/',
            }
        }
    }

    return JsonResponse(data, json_dumps_params={'indent': 2})


# Django REST Framework views for API endpoints
# Note: Uncomment these imports after installing djangorestframework
# from rest_framework import generics, viewsets
# from rest_framework.response import Response
# from .serializers import BookSerializer


# class BookList(generics.ListAPIView):
#     """
#     API view for listing all books.
#     GET: Returns a JSON list of all books in the database.
#
#     This view extends ListAPIView which provides:
#     - GET method to retrieve a list of books
#     - Automatic pagination (if configured)
#     - Filtering and searching capabilities
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# Temporary basic view for testing without DRF
def book_list_basic(request):
    """
    Basic view to list books in JSON format without DRF.
    This is a temporary implementation until DRF is installed.
    """
    books = Book.objects.all()
    books_data = []

    for book in books:
        books_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author
        })

    return JsonResponse({
        'count': len(books_data),
        'results': books_data,
        'message': 'Install djangorestframework and uncomment DRF views for full API functionality'
    }, json_dumps_params={'indent': 2})
#
# class BookViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for handling Book CRUD operations via API.
#     Provides list, create, retrieve, update, and delete operations.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
# class BookListCreateView(generics.ListCreateAPIView):
#     """
#     API view for listing and creating books.
#     GET: Returns a list of all books
#     POST: Creates a new book
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
# class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     API view for retrieving, updating, and deleting a specific book.
#     GET: Returns book details
#     PUT/PATCH: Updates book information
#     DELETE: Deletes the book
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
