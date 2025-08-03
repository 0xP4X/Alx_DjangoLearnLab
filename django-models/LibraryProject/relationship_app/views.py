from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.forms import ModelForm
from .models import Book, Author
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


# Book Form for CRUD operations

class BookForm(ModelForm):
    """Form for creating and editing Book instances"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['publication_year'].widget.attrs.update({'class': 'form-control'})


# Permission-secured views for Book CRUD operations

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View to add a new book - requires 'can_add_book' permission
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('list_books')
    else:
        form = BookForm()

    return render(request, 'relationship_app/add_book.html', {
        'form': form,
        'title': 'Add New Book'
    })


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book - requires 'can_change_book' permission
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)

    return render(request, 'relationship_app/edit_book.html', {
        'form': form,
        'book': book,
        'title': f'Edit Book: {book.title}'
    })


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book - requires 'can_delete_book' permission
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('list_books')

    return render(request, 'relationship_app/delete_book.html', {
        'book': book,
        'title': f'Delete Book: {book.title}'
    })
