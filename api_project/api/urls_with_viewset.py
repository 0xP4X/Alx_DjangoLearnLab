"""
Complete Django REST Framework URL configuration with ViewSet and DefaultRouter.
This file demonstrates the proper implementation as required by the task.

Usage: Replace the content of api/urls.py with this implementation after installing DRF.
"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSet with it
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')

# URL patterns for the API app
urlpatterns = [
    # Basic view to test the setup
    path('', views.api_home, name='api_home'),
    
    # Django REST Framework API endpoints with DefaultRouter
    # The router automatically creates the following URL patterns:
    # GET /books/ - List all books
    # POST /books/ - Create a new book
    # GET /books/{id}/ - Retrieve a specific book
    # PUT /books/{id}/ - Update a specific book (full update)
    # PATCH /books/{id}/ - Partial update of a specific book
    # DELETE /books/{id}/ - Delete a specific book
    path('', include(router.urls)),
    
    # Additional custom endpoints can be added here
    # path('books/search/', views.BookSearchView.as_view(), name='book-search'),
]

# The DefaultRouter automatically generates the following URL patterns:
# ^books/$ [name='book-list']
# ^books/(?P<pk>[^/.]+)/$ [name='book-detail']
# ^$ [name='api-root']

# Example API endpoints that will be available:
# GET    /api/books/          - List all books
# POST   /api/books/          - Create a new book
# GET    /api/books/1/        - Get book with ID 1
# PUT    /api/books/1/        - Update book with ID 1 (full update)
# PATCH  /api/books/1/        - Partially update book with ID 1
# DELETE /api/books/1/        - Delete book with ID 1
# GET    /api/                - API root view (provided by DefaultRouter)
