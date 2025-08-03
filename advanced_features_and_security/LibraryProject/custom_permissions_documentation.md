# Django Custom Permissions Implementation

## Objective
Implement custom permissions in Django application to control access to specific actions such as adding, editing, and deleting book entries based on user roles.

## Implementation Overview

### 1. Book Model with Custom Permissions

#### **Extended Book Model** (`models.py`):
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField(default=2000)

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
```

#### **Custom Permissions Defined**:
- ✅ **`can_add_book`** - Permission to add new books
- ✅ **`can_change_book`** - Permission to edit existing books  
- ✅ **`can_delete_book`** - Permission to delete books

### 2. Permission-Secured Views

#### **BookForm** (ModelForm for CRUD operations):
```python
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
```

#### **Permission-Secured Views**:

**Add Book View** (`add_book`):
- **Decorator**: `@permission_required('relationship_app.can_add_book', raise_exception=True)`
- **Purpose**: Create new book entries
- **Template**: `add_book.html`
- **Access**: Users with `can_add_book` permission only

**Edit Book View** (`edit_book`):
- **Decorator**: `@permission_required('relationship_app.can_change_book', raise_exception=True)`
- **Purpose**: Modify existing book entries
- **Template**: `edit_book.html`
- **Access**: Users with `can_change_book` permission only

**Delete Book View** (`delete_book`):
- **Decorator**: `@permission_required('relationship_app.can_delete_book', raise_exception=True)`
- **Purpose**: Remove book entries from database
- **Template**: `delete_book.html`
- **Access**: Users with `can_delete_book` permission only

### 3. URL Configuration

#### **Permission-Secured URLs** (`urls.py`):
```python
# Permission-secured book management URLs
path('add_book/', add_book, name='add_book'),
path('edit_book/<int:book_id>/', edit_book, name='edit_book'),
path('delete_book/<int:book_id>/', delete_book, name='delete_book'),
```

#### **Available URLs**:
- `/relationship_app/add_book/` - Add new book (requires `can_add_book`)
- `/relationship_app/edit_book/<id>/` - Edit book (requires `can_change_book`)
- `/relationship_app/delete_book/<id>/` - Delete book (requires `can_delete_book`)

### 4. Permission-Aware Templates

#### **Template Structure**:
```
relationship_app/templates/relationship_app/
├── add_book.html       # Add book form
├── edit_book.html      # Edit book form  
├── delete_book.html    # Delete confirmation
└── list_books.html     # Updated with permission checks
```

#### **Template Features**:

**Add Book Template** (`add_book.html`):
- Green color scheme (success theme)
- Form for creating new books
- Permission indicator message
- Form validation and error handling

**Edit Book Template** (`edit_book.html`):
- Yellow color scheme (warning theme)
- Pre-populated form with existing book data
- Current book information display
- Update confirmation

**Delete Book Template** (`delete_book.html`):
- Red color scheme (danger theme)
- Book details confirmation
- Warning message about permanent deletion
- Confirmation form

**Updated List Books Template** (`list_books.html`):
- Permission-aware action buttons
- Conditional display based on user permissions
- Enhanced layout with book cards
- CRUD operation links

### 5. Permission System Architecture

#### **Permission Hierarchy**:

**Admin Users**:
- ✅ `can_add_book` - Can create new books
- ✅ `can_change_book` - Can edit existing books
- ✅ `can_delete_book` - Can delete books
- **Full CRUD access** to book management

**Librarian Users**:
- ✅ `can_add_book` - Can create new books
- ✅ `can_change_book` - Can edit existing books
- ❌ `can_delete_book` - Cannot delete books
- **Create, Read, Update access** (no delete)

**Member Users**:
- ❌ `can_add_book` - Cannot create books
- ❌ `can_change_book` - Cannot edit books
- ❌ `can_delete_book` - Cannot delete books
- **Read-only access** to book information

### 6. Security Features

#### **Permission Enforcement**:
- **`@permission_required` decorator** on all CRUD views
- **`raise_exception=True`** for proper error handling
- **Template permission checks** using `{% if perms.app.permission %}`
- **Automatic redirect** to login for unauthorized users

#### **Form Security**:
- **CSRF protection** on all forms
- **Form validation** with error display
- **GET/POST method handling** for proper form submission
- **Object existence verification** with `get_object_or_404`

### 7. Database Migration

#### **Migration Details**:
- **Migration created**: `0004_alter_book_options.py`
- **Changes**: Added custom permissions to Book model Meta class
- **Applied successfully** to database
- **Permissions available** in Django admin and programmatically

### 8. Permission Assignment

#### **Automated Permission Setup**:
- **Script**: `setup_permissions.py` for automated permission assignment
- **Admin users**: All book permissions (add, change, delete)
- **Librarian users**: Add and change permissions only
- **Member users**: No special permissions (read-only)

#### **Permission Verification**:
- ✅ Admin: Full CRUD access confirmed
- ✅ Librarian: Create/Update access confirmed, no delete
- ✅ Member: Read-only access confirmed

### 9. User Experience

#### **Permission-Aware Interface**:
- **Conditional buttons** - Only show actions user can perform
- **Clear permission indicators** in templates
- **Intuitive navigation** based on user capabilities
- **Consistent styling** across all CRUD operations

#### **Error Handling**:
- **Permission denied** pages for unauthorized access
- **Form validation** with clear error messages
- **Confirmation dialogs** for destructive operations
- **Success redirects** after successful operations

### 10. Testing and Verification

#### **Test Users with Permissions**:
- **admin_user**: Full book management permissions
- **librarian_user**: Add and edit permissions only
- **member_user**: Read-only access

#### **Functional Testing**:
- ✅ Permission decorators working correctly
- ✅ Template permission checks functioning
- ✅ Form submissions and validations working
- ✅ CRUD operations properly secured
- ✅ Unauthorized access properly blocked

## Conclusion

The custom permissions system is fully implemented with:
- ✅ **Custom permissions** defined in Book model Meta class
- ✅ **Permission-secured views** using `@permission_required` decorator
- ✅ **Proper URL routing** for secured book management operations
- ✅ **Permission-aware templates** with conditional display
- ✅ **Role-based permission assignment** (Admin, Librarian, Member)
- ✅ **Comprehensive CRUD operations** with proper security
- ✅ **Database migration** applied successfully
- ✅ **Automated permission setup** script
- ✅ **Complete testing and verification**

Users now have granular access control for book management operations based on their assigned permissions, ensuring proper security and user experience.
