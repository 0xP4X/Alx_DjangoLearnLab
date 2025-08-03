from django.urls import path
from . import views

# Edit relationship_app/urls.py to include URL patterns that route to the newly created views.
# Make sure to link both the function-based and class-based views.
urlpatterns = [
    # Function-based view for listing all books - Make sure to link both the function-based and class-based views
    path('books/', views.list_books, name='list_books'),

    # Class-based view for library detail - Make sure to link both the function-based and class-based views
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
