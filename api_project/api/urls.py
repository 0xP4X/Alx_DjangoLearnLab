"""
URL configuration for the API app.
This module will contain URL patterns for API endpoints once Django REST Framework is integrated.
"""

from django.urls import path
from . import views

# URL patterns for the API app
# These will be expanded once Django REST Framework is integrated
urlpatterns = [
    # Basic view to test the setup
    path('', views.api_home, name='api_home'),

    # Temporary basic book list (until DRF is installed)
    path('books/', views.book_list_basic, name='book-list-basic'),

    # Django REST Framework API endpoints (uncomment after installing DRF):
    # path('books/', views.BookList.as_view(), name='book-list'),  # Maps to the BookList view

    # Future API endpoints:
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
