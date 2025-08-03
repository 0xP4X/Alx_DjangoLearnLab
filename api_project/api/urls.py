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
    
    # Future API endpoints (to be implemented with DRF):
    # path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
