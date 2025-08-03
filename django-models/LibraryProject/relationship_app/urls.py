from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# Edit relationship_app/urls.py to include URL patterns that route to the newly created views.
# Make sure to link both the function-based and class-based views.
urlpatterns = [
    # Function-based view for listing all books - Make sure to link both the function-based and class-based views
    path('books/', list_books, name='list_books'),

    # Class-based view for library detail - Make sure to link both the function-based and class-based views
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
