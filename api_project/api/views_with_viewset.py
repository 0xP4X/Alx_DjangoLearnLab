"""
Complete Django REST Framework ViewSet implementation.
This file demonstrates the proper BookViewSet implementation as required by the task.

Usage: Replace the DRF views in api/views.py with this implementation after installing DRF.
"""

from django.shortcuts import render
from django.http import JsonResponse
from .models import Book

# Django REST Framework views for API endpoints
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Book CRUD operations via API.
    
    This ViewSet automatically provides the following endpoints:
    - GET /books/ - List all books
    - POST /books/ - Create a new book
    - GET /books/{id}/ - Retrieve a specific book
    - PUT /books/{id}/ - Update a specific book (full update)
    - PATCH /books/{id}/ - Partial update of a specific book
    - DELETE /books/{id}/ - Delete a specific book
    
    The ViewSet uses the DefaultRouter to automatically generate URL patterns.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def list(self, request):
        """
        List all books.
        Override the default list method to add custom behavior if needed.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    def create(self, request):
        """
        Create a new book.
        Override the default create method to add custom behavior if needed.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific book by ID.
        Override the default retrieve method to add custom behavior if needed.
        """
        book = self.get_object()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """
        Update a specific book (full update).
        Override the default update method to add custom behavior if needed.
        """
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """
        Partially update a specific book.
        Override the default partial_update method to add custom behavior if needed.
        """
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete a specific book.
        Override the default destroy method to add custom behavior if needed.
        """
        book = self.get_object()
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom action to search books by title or author.
        Accessible at: GET /books/search/?q=search_term
        """
        query = request.query_params.get('q', '')
        if query:
            books = self.queryset.filter(
                title__icontains=query
            ) | self.queryset.filter(
                author__icontains=query
            )
        else:
            books = self.queryset.none()
        
        serializer = self.get_serializer(books, many=True)
        return Response({
            'query': query,
            'count': books.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """
        Custom action to get a summary of a specific book.
        Accessible at: GET /books/{id}/summary/
        """
        book = self.get_object()
        return Response({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'summary': f"'{book.title}' is a book written by {book.author}."
        })


class BookListCreateView(generics.ListCreateAPIView):
    """
    Alternative API view for listing and creating books (ListCreateAPIView approach).
    This is an alternative to the ViewSet approach above.
    
    Provides:
    - GET /books/ - List all books
    - POST /books/ - Create a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Alternative API view for retrieving, updating, and deleting a specific book.
    This is an alternative to the ViewSet approach above.
    
    Provides:
    - GET /books/{id}/ - Retrieve a specific book
    - PUT /books/{id}/ - Update a specific book
    - PATCH /books/{id}/ - Partially update a specific book
    - DELETE /books/{id}/ - Delete a specific book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Basic view for testing without DRF (keep this for fallback)
def api_home(request):
    """
    Basic API home view for testing the setup.
    This provides information about the API and available endpoints.
    """
    # Get basic statistics
    book_count = Book.objects.count()
    
    # Return basic API information
    data = {
        'message': 'Welcome to the Django REST Framework API Project',
        'status': 'DRF Active with ViewSet',
        'django_version': '5.2.4',
        'api_app': 'Active',
        'book_count': book_count,
        'viewset_features': [
            'Full CRUD operations via ViewSet',
            'DefaultRouter URL generation',
            'Automatic API endpoint creation',
            'Custom actions for search and summary'
        ],
        'endpoints': {
            'books_list': '/api/books/ (GET, POST)',
            'book_detail': '/api/books/{id}/ (GET, PUT, PATCH, DELETE)',
            'book_search': '/api/books/search/?q=term (GET)',
            'book_summary': '/api/books/{id}/summary/ (GET)',
            'api_root': '/api/ (GET)',
            'admin': '/admin/',
        }
    }
    
    return JsonResponse(data, json_dumps_params={'indent': 2})


def book_list_basic(request):
    """
    Basic view to list books in JSON format without DRF.
    This is a fallback implementation.
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
        'message': 'Basic implementation - DRF ViewSet available at /api/books/'
    }, json_dumps_params={'indent': 2})
