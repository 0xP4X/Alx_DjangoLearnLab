from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from .models import Book
from .models import Library

# Create your views here.

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    This view should render a simple text list of book titles and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
# Utilize Django's ListView or DetailView to structure this class-based view
class LibraryDetailView(DetailView):
    """
    Create a class-based view in relationship_app/views.py that displays details for a specific library,
    listing all books available in that library.
    Utilize Django's ListView or DetailView to structure this class-based view.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Authentication Views

def register(request):
    """
    User registration view using Django's built-in UserCreationForm
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')  # Redirect to books list after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view using Django's built-in LoginView
    """
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/relationship_app/books/'  # Redirect to books list after login


class CustomLogoutView(LogoutView):
    """
    Custom logout view using Django's built-in LogoutView
    """
    template_name = 'relationship_app/logout.html'


# Role-based access control helper functions

def is_admin(user):
    """Check if user has Admin role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    """Check if user has Librarian role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    """Check if user has Member role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Role-based views with access restrictions

@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin view that only users with the 'Admin' role can access
    """
    return render(request, 'relationship_app/admin_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'No Role'
    })


@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian view accessible only to users identified as 'Librarians'
    """
    return render(request, 'relationship_app/librarian_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'No Role'
    })


@user_passes_test(is_member)
def member_view(request):
    """
    Member view for users with the 'Member' role
    """
    return render(request, 'relationship_app/member_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'No Role'
    })
