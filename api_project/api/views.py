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


# Future DRF views will be implemented here:
#
# from rest_framework import generics, viewsets
# from rest_framework.response import Response
# from .serializers import BookSerializer
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
