# Django Permissions and Groups Implementation Guide

## Objective
Implement and manage permissions and groups to control access to various parts of the Django application, enhancing security and functionality through detailed access controls based on user roles and their assigned permissions.

## Implementation Overview

This system demonstrates a comprehensive approach to Django permissions and groups, utilizing both function-based and class-based views with permission enforcement.

## Step 1: Custom Permissions in Models ✅

### **Book Model with Custom Permissions** (`bookshelf/models.py`):
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

### **Custom Permissions Defined**:
- ✅ **`can_view`** - Permission to view books
- ✅ **`can_create`** - Permission to create new books
- ✅ **`can_edit`** - Permission to edit existing books
- ✅ **`can_delete`** - Permission to delete books

## Step 2: Groups and Permissions Setup ✅

### **Groups Created**:

#### **1. Viewers Group**
- **Permissions**: `can_view`
- **Access Level**: Read-only access to books
- **Use Case**: Users who can only browse and view book information

#### **2. Editors Group**
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Access Level**: Create, read, and update access
- **Use Case**: Content managers who can add and modify books

#### **3. Admins Group**
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Access Level**: Full CRUD access
- **Use Case**: System administrators with complete control

### **Setup Command**:
```bash
python manage.py setup_groups
```

## Step 3: Permission Enforcement in Views ✅

### **Function-Based Views with @permission_required**:

```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View to list all books - requires 'can_view' permission"""

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View to create a new book - requires 'can_create' permission"""

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """View to edit an existing book - requires 'can_edit' permission"""

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """View to delete a book - requires 'can_delete' permission"""
```

### **Class-Based Views with PermissionRequiredMixin**:

```python
class BookListView(PermissionRequiredMixin, ListView):
    permission_required = 'bookshelf.can_view'
    raise_exception = True

class BookCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'bookshelf.can_create'
    raise_exception = True

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'bookshelf.can_edit'
    raise_exception = True

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'bookshelf.can_delete'
    raise_exception = True
```

## Step 4: Testing Implementation ✅

### **Test Users Created**:

#### **Test User Accounts**:
- **`viewer_user`** / `viewer123` - Assigned to Viewers group
- **`editor_user`** / `editor123` - Assigned to Editors group  
- **`admin_user`** / `admin123` - Assigned to Admins group

### **Testing Approach**:
1. **Create test users** and assign them to different groups
2. **Log in as these users** and attempt to access various parts of the application
3. **Verify that permissions are applied correctly**

### **Setup Test Users**:
```bash
python manage.py create_test_users
```

### **Manual Testing Steps**:

#### **1. Viewer User Testing**:
- ✅ Can access book list (`/bookshelf/`)
- ✅ Can view book details
- ❌ Cannot create new books (no "Add New Book" button)
- ❌ Cannot edit books (no "Edit" buttons)
- ❌ Cannot delete books (no "Delete" buttons)

#### **2. Editor User Testing**:
- ✅ Can access book list
- ✅ Can view book details
- ✅ Can create new books
- ✅ Can edit existing books
- ❌ Cannot delete books (no "Delete" buttons)

#### **3. Admin User Testing**:
- ✅ Can access book list
- ✅ Can view book details
- ✅ Can create new books
- ✅ Can edit existing books
- ✅ Can delete books

## URL Patterns

### **Function-Based Views**:
```python
urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
]
```

### **Class-Based Views** (Alternative Implementation):
```python
urlpatterns = [
    path('cbv/', views.BookListView.as_view(), name='book_list_cbv'),
    path('cbv/book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail_cbv'),
    path('cbv/book/create/', views.BookCreateView.as_view(), name='book_create_cbv'),
    path('cbv/book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit_cbv'),
    path('cbv/book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete_cbv'),
]
```

## Permission-Aware Templates

### **Template Features**:
- **Permission Badges**: Visual indicators of user permissions
- **Conditional Buttons**: Only show actions user can perform
- **Dynamic Styling**: Different colors based on permission levels
- **User Feedback**: Clear indication of access levels

### **Template Permission Checks**:
```html
{% if user_permissions.can_create %}
    <a href="{% url 'book_create' %}" class="btn btn-success">➕ Add New Book</a>
{% endif %}

{% if user_permissions.can_edit %}
    <a href="{% url 'book_edit' book.pk %}" class="btn btn-warning">✏️ Edit</a>
{% endif %}

{% if user_permissions.can_delete %}
    <a href="{% url 'book_delete' book.pk %}" class="btn btn-danger">🗑️ Delete</a>
{% endif %}
```

## Security Features

### **Permission Enforcement**:
- ✅ **`@permission_required` decorator** on function-based views
- ✅ **`PermissionRequiredMixin`** on class-based views
- ✅ **`raise_exception=True`** for proper error handling
- ✅ **Template permission checks** for UI elements
- ✅ **Group-based permission assignment**

### **Access Control Levels**:
1. **Model Level**: Custom permissions defined in model Meta class
2. **View Level**: Permission decorators and mixins
3. **Template Level**: Conditional display based on permissions
4. **Group Level**: Organized permission sets for different user roles

## Management Commands

### **Available Commands**:
```bash
# Set up groups and assign permissions
python manage.py setup_groups

# Create test users and assign to groups
python manage.py create_test_users

# Apply database migrations
python manage.py migrate
```

## File Structure

```
bookshelf/
├── models.py                          # Book model with custom permissions
├── views.py                           # Permission-protected views
├── urls.py                            # URL routing
├── admin.py                           # Admin configuration
├── management/
│   └── commands/
│       ├── setup_groups.py            # Groups and permissions setup
│       └── create_test_users.py       # Test user creation
└── templates/bookshelf/
    ├── book_list.html                 # Permission-aware book list
    ├── book_form.html                 # Create/edit form
    └── book_confirm_delete.html       # Delete confirmation
```

## Testing URLs

- **Book List**: `/bookshelf/` (requires `can_view`)
- **Create Book**: `/bookshelf/book/create/` (requires `can_create`)
- **Edit Book**: `/bookshelf/book/<id>/edit/` (requires `can_edit`)
- **Delete Book**: `/bookshelf/book/<id>/delete/` (requires `can_delete`)
- **Class-Based Views**: `/bookshelf/cbv/` (alternative implementation)

## Conclusion

This implementation provides a comprehensive permissions and groups system with:

- ✅ **Custom model permissions** for granular access control
- ✅ **Group-based permission management** for easy user organization
- ✅ **Permission enforcement in views** using decorators and mixins
- ✅ **Permission-aware templates** for dynamic UI
- ✅ **Test users and data** for verification
- ✅ **Management commands** for easy setup
- ✅ **Comprehensive documentation** for maintenance

The system demonstrates Django's powerful permission framework and provides a solid foundation for role-based access control in web applications.
