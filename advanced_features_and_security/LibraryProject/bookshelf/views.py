from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import Http404
import logging

from .models import Book
from .forms import SecureBookForm, SecureSearchForm

# Configure security logging
logger = logging.getLogger('django.security')


# Use the secure form for all CRUD operations
BookForm = SecureBookForm


# Permission-protected views using function-based approach

@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
@never_cache
def book_list(request):
    """
    Secure view to list all books with search functionality.
    Demonstrates permission enforcement and secure data access.

    Security Features:
    - Permission-based access control
    - CSRF protection for search forms
    - Input validation and sanitization
    - SQL injection prevention via Django ORM
    - XSS prevention via template escaping
    """
    books = Book.objects.all()
    search_form = SecureSearchForm()
    search_query = None

    # Handle secure search functionality
    if request.method == 'GET' and 'query' in request.GET:
        search_form = SecureSearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            search_type = search_form.cleaned_data['search_type']
            search_query = query

            # Use Django ORM for secure database queries (prevents SQL injection)
            if search_type == 'title':
                books = books.filter(title__icontains=query)
            elif search_type == 'author':
                books = books.filter(author__icontains=query)
            else:  # both
                books = books.filter(
                    Q(title__icontains=query) | Q(author__icontains=query)
                )

            # Log search activity for security monitoring
            logger.info(f'User {request.user.username} searched for: {query}')
        else:
            # Log invalid search attempts
            logger.warning(f'Invalid search attempt by user {request.user.username}: {request.GET}')

    # Implement pagination for performance and security
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bookshelf/book_list.html', {
        'books': page_obj,
        'search_form': search_form,
        'search_query': search_query,
        'title': 'Book Library',
        'user_permissions': {
            'can_view': request.user.has_perm('bookshelf.can_view'),
            'can_create': request.user.has_perm('bookshelf.can_create'),
            'can_edit': request.user.has_perm('bookshelf.can_edit'),
            'can_delete': request.user.has_perm('bookshelf.can_delete'),
        }
    })


@permission_required('bookshelf.can_view', raise_exception=True)
@never_cache
def book_detail(request, pk):
    """
    Secure view to display book details with enhanced security.

    Security Features:
    - Permission-based access control
    - Secure object retrieval with 404 handling
    - Input validation for primary key
    - Activity logging for security monitoring
    """
    try:
        # Validate pk parameter to prevent injection
        pk = int(pk)
        if pk <= 0:
            raise Http404("Invalid book ID")

        book = get_object_or_404(Book, pk=pk)

        # Log book access for security monitoring
        logger.info(f'User {request.user.username} accessed book: {book.title} (ID: {pk})')

        return render(request, 'bookshelf/book_detail.html', {
            'book': book,
            'title': f'Book: {book.title}',
            'user_permissions': {
                'can_view': request.user.has_perm('bookshelf.can_view'),
                'can_create': request.user.has_perm('bookshelf.can_create'),
                'can_edit': request.user.has_perm('bookshelf.can_edit'),
                'can_delete': request.user.has_perm('bookshelf.can_delete'),
            }
        })
    except (ValueError, TypeError):
        logger.warning(f'Invalid book ID access attempt by user {request.user.username}: {pk}')
        raise Http404("Invalid book ID")


@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
def book_create(request):
    """
    Secure view to create a new book with comprehensive validation.

    Security Features:
    - Permission-based access control
    - CSRF protection for form submissions
    - Input validation and sanitization via SecureBookForm
    - Activity logging for security monitoring
    - Secure error handling
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                book = form.save()

                # Log successful book creation
                logger.info(f'User {request.user.username} created book: {book.title}')

                messages.success(request, f'Book "{book.title}" created successfully!')
                return redirect('book_detail', pk=book.pk)
            except Exception as e:
                # Log creation errors for security monitoring
                logger.error(f'Book creation error for user {request.user.username}: {str(e)}')
                messages.error(request, 'An error occurred while creating the book. Please try again.')
        else:
            # Log form validation errors
            logger.warning(f'Invalid book creation attempt by user {request.user.username}: {form.errors}')
    else:
        form = BookForm()

    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Create New Book',
        'action': 'Create'
    })


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book - requires 'can_edit' permission.
    Example: Use @permission_required('app_name.can_edit', raise_exception=True) to protect an edit view.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'title': f'Edit Book: {book.title}',
        'action': 'Update'
    })


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book - requires 'can_delete' permission.
    Ensures views that delete model instances check for the correct permissions.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/book_confirm_delete.html', {
        'book': book,
        'title': f'Delete Book: {book.title}'
    })


# Permission-protected class-based views using PermissionRequiredMixin

class BookListView(PermissionRequiredMixin, ListView):
    """
    Class-based view to list all books - requires 'can_view' permission.
    Demonstrates permission enforcement using PermissionRequiredMixin.
    """
    model = Book
    template_name = 'bookshelf/book_list_cbv.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Book Library (Class-Based View)'
        context['user_permissions'] = {
            'can_view': self.request.user.has_perm('bookshelf.can_view'),
            'can_create': self.request.user.has_perm('bookshelf.can_create'),
            'can_edit': self.request.user.has_perm('bookshelf.can_edit'),
            'can_delete': self.request.user.has_perm('bookshelf.can_delete'),
        }
        return context


class BookDetailView(PermissionRequiredMixin, DetailView):
    """
    Class-based view to display book details - requires 'can_view' permission.
    """
    model = Book
    template_name = 'bookshelf/book_detail_cbv.html'
    context_object_name = 'book'
    permission_required = 'bookshelf.can_view'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Book: {self.object.title} (Class-Based View)'
        context['user_permissions'] = {
            'can_view': self.request.user.has_perm('bookshelf.can_view'),
            'can_create': self.request.user.has_perm('bookshelf.can_create'),
            'can_edit': self.request.user.has_perm('bookshelf.can_edit'),
            'can_delete': self.request.user.has_perm('bookshelf.can_delete'),
        }
        return context


class BookCreateView(PermissionRequiredMixin, CreateView):
    """
    Class-based view to create a new book - requires 'can_create' permission.
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form_cbv.html'
    permission_required = 'bookshelf.can_create'
    raise_exception = True
    success_url = reverse_lazy('book_list_cbv')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Book (Class-Based View)'
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Book "{form.instance.title}" created successfully!')
        return super().form_valid(form)


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Class-based view to edit an existing book - requires 'can_edit' permission.
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form_cbv.html'
    permission_required = 'bookshelf.can_edit'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Book: {self.object.title} (Class-Based View)'
        context['action'] = 'Update'
        return context

    def get_success_url(self):
        return reverse_lazy('book_detail_cbv', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Book "{form.instance.title}" updated successfully!')
        return super().form_valid(form)


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Class-based view to delete a book - requires 'can_delete' permission.
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete_cbv.html'
    permission_required = 'bookshelf.can_delete'
    raise_exception = True
    success_url = reverse_lazy('book_list_cbv')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete Book: {self.object.title} (Class-Based View)'
        return context

    def delete(self, request, *args, **kwargs):
        book_title = self.get_object().title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return response


def form_example(request):
    """
    Security demonstration view showing secure form implementation.
    This view demonstrates various security features and best practices.
    """
    return render(request, 'bookshelf/form_example.html', {
        'title': 'Secure Form Example',
    })
