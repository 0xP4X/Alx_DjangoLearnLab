from django.urls import path
from . import views

# Edit relationship_app/urls.py to include URL patterns that route to the newly created views.
# Make sure to link both the function-based and class-based views.
urlpatterns = [
    # Function-based view for listing all books
    path('books/', views.list_books, name='list_books'),

    # Class-based view for library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
