"""
URL configuration for the bookshelf app.
Defines URL patterns for permission-protected views demonstrating
both function-based and class-based view approaches.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Function-based views with permission protection
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Class-based views with permission protection (alternative implementation)
    path('cbv/', views.BookListView.as_view(), name='book_list_cbv'),
    path('cbv/book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail_cbv'),
    path('cbv/book/create/', views.BookCreateView.as_view(), name='book_create_cbv'),
    path('cbv/book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit_cbv'),
    path('cbv/book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete_cbv'),
]
