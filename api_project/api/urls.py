"""
URL configuration for the API app.
This module contains URL patterns for API endpoints using Django REST Framework.
"""

from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSet with it (uncomment after installing DRF)
# router = DefaultRouter()
# router.register(r'books', views.BookViewSet, basename='book')

# URL patterns for the API app
# These will be expanded once Django REST Framework is integrated
urlpatterns = [
    # Basic view to test the setup
    path('', views.api_home, name='api_home'),

    # Temporary basic book list (until DRF is installed)
    path('books/', views.book_list_basic, name='book-list-basic'),

    # Django REST Framework API endpoints with DefaultRouter (uncomment after installing DRF)
    # The router URLs will include:
    # GET/POST /books/ - List/Create books
    # GET/PUT/PATCH/DELETE /books/{id}/ - Retrieve/Update/Delete specific book
    # path('', include(router.urls)),
]
