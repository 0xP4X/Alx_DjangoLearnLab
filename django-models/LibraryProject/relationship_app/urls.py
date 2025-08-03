from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import admin_view, librarian_view, member_view
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

    # Role-based access control URLs
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
]
