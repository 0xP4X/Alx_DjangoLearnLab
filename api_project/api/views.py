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
# from rest_framework import generics, viewsets, permissions
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .serializers import BookSerializer
# from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly


# # class BookViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for handling Book CRUD operations via API with authentication and permissions.
#     Provides list, create, retrieve, update, and delete operations.
#
#     This ViewSet automatically provides:
#     - GET /books/ - List all books (public access)
#     - POST /books/ - Create a new book (authenticated users only)
#     - GET /books/{id}/ - Retrieve a specific book (public access)
#     - PUT /books/{id}/ - Update a specific book (authenticated users only)
#     - DELETE /books/{id}/ - Delete a specific book (admin users only)
#
#     Authentication: Token, Session, Basic
#     Permissions: Custom permissions based on action
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def get_permissions(self):
#         """
#         Instantiates and returns the list of permissions that this view requires.
#         Different permissions for different actions.
#         """
#         if self.action == 'list' or self.action == 'retrieve':
#             # Anyone can read books
#             permission_classes = [permissions.AllowAny]
#         elif self.action == 'create':
#             # Only authenticated users can create books
#             permission_classes = [permissions.IsAuthenticated]
#         elif self.action == 'update' or self.action == 'partial_update':
#             # Only authenticated users can update books
#             permission_classes = [permissions.IsAuthenticated]
#         elif self.action == 'destroy':
#             # Only admin users can delete books
#             permission_classes = [permissions.IsAdminUser]
#         else:
#             # Default to authenticated users for custom actions
#             permission_classes = [permissions.IsAuthenticated]
#
#         return [permission() for permission in permission_classes]
#
#     @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
#     def public_books(self, request):
#         """
#         Custom action to get public books (no authentication required).
#         GET /books/public_books/
#         """
#         books = self.get_queryset()
#         serializer = self.get_serializer(books, many=True)
#         return Response({
#             'count': books.count(),
#             'results': serializer.data,
#             'message': 'Public access to books'
#         })
#
#     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
#     def my_books(self, request):
#         """
#         Custom action to get books for authenticated user.
#         GET /books/my_books/
#         Headers: Authorization: Token your_token
#         """
#         # For now, return all books since we don't have user-book relationship
#         books = self.get_queryset()
#         serializer = self.get_serializer(books, many=True)
#         return Response({
#             'count': books.count(),
#             'results': serializer.data,
#             'user': request.user.username,
#             'message': 'Books accessible to authenticated user'
#         })
#
#     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
#     def admin_stats(self, request):
#         """
#         Custom action for admin statistics.
#         GET /books/admin_stats/
#         Headers: Authorization: Token admin_token
#         """
#         books = self.get_queryset()
#         return Response({
#             'total_books': books.count(),
#             'admin_user': request.user.username,
#             'message': 'Admin-only statistics'
#         })


# class BookList(generics.ListAPIView):
#     """
#     Alternative API view for listing all books (ListAPIView approach).
#     GET: Returns a JSON list of all books in the database.
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
