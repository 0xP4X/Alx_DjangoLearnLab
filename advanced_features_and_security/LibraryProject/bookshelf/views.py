from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib import messages
from .models import Book


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


# Permission-protected views using function-based approach

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books - requires 'can_view' permission.
    Demonstrates permission enforcement in views using @permission_required decorator.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'title': 'Book Library',
        'user_permissions': {
            'can_view': request.user.has_perm('bookshelf.can_view'),
            'can_create': request.user.has_perm('bookshelf.can_create'),
            'can_edit': request.user.has_perm('bookshelf.can_edit'),
            'can_delete': request.user.has_perm('bookshelf.can_delete'),
        }
    })


@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    View to display book details - requires 'can_view' permission.
    Example: Use @permission_required('app_name.can_view', raise_exception=True) to protect a view.
    """
    book = get_object_or_404(Book, pk=pk)
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


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book - requires 'can_create' permission.
    Ensures views that create model instances check for the correct permissions.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', pk=book.pk)
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
