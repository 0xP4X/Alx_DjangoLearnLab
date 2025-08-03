# Django Role-Based Access Control Implementation

## Objective
Implement role-based access control within a Django application to manage different user roles and permissions effectively by extending the User model and creating views that restrict access based on user roles.

## Implementation Overview

### 1. UserProfile Model Extension

#### **UserProfile Model** (`models.py`):
```python
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
```

#### **Key Features**:
- **One-to-One Relationship**: Links to Django's built-in User model
- **Role Field**: CharField with predefined choices (Admin, Librarian, Member)
- **Default Role**: New users automatically assigned 'Member' role
- **Automatic Creation**: Django signals create UserProfile when User is created

#### **Django Signals** (Automatic UserProfile Creation):
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)
```

### 2. Role-Based Views with Access Control

#### **Role Checking Functions**:
```python
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'
```

#### **Protected Views**:

**Admin View** (`admin_view`):
- **Access**: Only users with 'Admin' role
- **Decorator**: `@user_passes_test(is_admin)`
- **Template**: `admin_view.html`
- **Features**: User management, role assignment, system configuration

**Librarian View** (`librarian_view`):
- **Access**: Only users with 'Librarian' role
- **Decorator**: `@user_passes_test(is_librarian)`
- **Template**: `librarian_view.html`
- **Features**: Book management, member management, library operations

**Member View** (`member_view`):
- **Access**: Only users with 'Member' role
- **Decorator**: `@user_passes_test(is_member)`
- **Template**: `member_view.html`
- **Features**: Browse books, view details, reading history

### 3. URL Configuration

#### **Role-Based URLs** (`urls.py`):
```python
# Role-based access control URLs
path('admin/', admin_view, name='admin_view'),
path('librarian/', librarian_view, name='librarian_view'),
path('member/', member_view, name='member_view'),
```

#### **Available URLs**:
- `/relationship_app/admin/` - Admin dashboard (Admin role only)
- `/relationship_app/librarian/` - Librarian dashboard (Librarian role only)
- `/relationship_app/member/` - Member dashboard (Member role only)

### 4. Role-Based HTML Templates

#### **Template Structure**:
```
relationship_app/templates/relationship_app/
├── admin_view.html      # Admin dashboard
├── librarian_view.html  # Librarian dashboard
├── member_view.html     # Member dashboard
├── login.html
├── logout.html
├── register.html
├── list_books.html
└── library_detail.html
```

#### **Template Features**:

**Admin Template** (`admin_view.html`):
- Red color scheme (danger/admin theme)
- Admin-specific features and capabilities
- Navigation to all other views
- User management tools

**Librarian Template** (`librarian_view.html`):
- Green color scheme (success/library theme)
- Library management features
- Book and member management tools
- Navigation to member view

**Member Template** (`member_view.html`):
- Blue color scheme (primary/member theme)
- Member-focused features
- Book browsing and reading tools
- Limited navigation options

### 5. Security and Access Control

#### **Access Control Mechanism**:
- **Decorator**: `@user_passes_test()` with custom role checking functions
- **Authentication Required**: All role-based views require login
- **Role Verification**: Each view checks specific role before granting access
- **Automatic Redirect**: Unauthorized users redirected to login page

#### **Role Hierarchy**:
1. **Admin**: Highest level access
   - User management and role assignment
   - System configuration and settings
   - Full library management access
   - Access to all views

2. **Librarian**: Library management access
   - Book catalog management
   - Member account management
   - Library operations and reports
   - Limited administrative functions

3. **Member**: Basic user access
   - Browse and search books
   - View book details and library information
   - Personal account management
   - Reading history and recommendations

### 6. Test Users Created

#### **Test Accounts**:
- **Admin User**: `admin_user` / `admin123` (Admin role)
- **Librarian User**: `librarian_user` / `librarian123` (Librarian role)
- **Member User**: `member_user` / `member123` (Member role)

### 7. Testing and Verification

#### **Role Function Testing**:
- ✅ `is_admin()` correctly identifies Admin users
- ✅ `is_librarian()` correctly identifies Librarian users
- ✅ `is_member()` correctly identifies Member users
- ✅ Cross-role verification prevents unauthorized access

#### **Access Control Testing**:
- ✅ Admin users can access admin_view
- ✅ Librarian users can access librarian_view
- ✅ Member users can access member_view
- ✅ Unauthorized users redirected to login

### 8. Integration with Existing System

#### **Seamless Integration**:
- Works with existing authentication system
- Compatible with existing book/library models
- Maintains existing URL structure
- Preserves all current functionality

#### **Database Migration**:
- Migration created: `0003_userprofile.py`
- UserProfile table added to database
- Existing users automatically get UserProfile with 'Member' role

### 9. Future Enhancements

#### **Potential Improvements**:
- Permission-based access control (Django permissions)
- Group-based role management
- Role inheritance and hierarchies
- Audit logging for role changes
- API endpoints with role-based access
- Dynamic role assignment interface

## Conclusion

The role-based access control system is fully implemented with:
- ✅ UserProfile model extending Django User
- ✅ Three distinct user roles (Admin, Librarian, Member)
- ✅ Automatic UserProfile creation via Django signals
- ✅ Role-specific views with access restrictions
- ✅ Custom role checking functions
- ✅ @user_passes_test decorators for access control
- ✅ Role-specific HTML templates with unique designs
- ✅ Proper URL routing for role-based views
- ✅ Test users for each role
- ✅ Complete integration with existing authentication

Users now have role-based access to different parts of the application, ensuring proper security and user experience based on their assigned roles.
