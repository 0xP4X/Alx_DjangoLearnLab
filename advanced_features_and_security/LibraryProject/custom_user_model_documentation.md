# Django Custom User Model Implementation

## Objective
Customize Django's user model to suit the specific needs of the application, demonstrating an understanding of extending Django's authentication system by replacing Django's default user model with a custom user model that includes additional fields and functionality.

## Implementation Overview

### Project Structure
```
advanced_features_and_security/
└── LibraryProject/
    ├── accounts/                    # New app for custom user model
    │   ├── models.py               # Custom user model and manager
    │   ├── admin.py                # Custom admin configuration
    │   └── migrations/
    ├── LibraryProject/
    │   └── settings.py             # Updated with AUTH_USER_MODEL
    └── relationship_app/           # Updated to use custom user
        └── models.py               # Updated user references
```

## Step 1: Custom User Model Setup ✅

### **CustomUser Model** (`accounts/models.py`):
```python
class CustomUser(AbstractUser):
    # Additional fields beyond Django's built-in user model
    date_of_birth = models.DateField(
        _('Date of Birth'),
        null=True,
        blank=True,
        help_text=_('Enter your date of birth')
    )
    
    profile_photo = models.ImageField(
        _('Profile Photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text=_('Upload a profile photo')
    )
    
    # Use the custom user manager
    objects = CustomUserManager()
```

### **Key Features**:
- ✅ **Extends AbstractUser** - Inherits all Django user functionality
- ✅ **date_of_birth field** - DateField for storing birth dates
- ✅ **profile_photo field** - ImageField for user profile photos
- ✅ **Custom properties** - Age calculation, full name methods
- ✅ **Internationalization** - Uses gettext_lazy for translations

## Step 2: Settings Configuration ✅

### **Settings Updates** (`LibraryProject/settings.py`):
```python
# Custom User Model Configuration
AUTH_USER_MODEL = 'accounts.CustomUser'

# Media files configuration for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

INSTALLED_APPS = [
    # ... other apps
    'accounts',  # Custom user model app
    # ... other apps
]
```

### **Configuration Features**:
- ✅ **AUTH_USER_MODEL** - Points to custom user model
- ✅ **Media configuration** - For profile photo uploads
- ✅ **App registration** - Accounts app added to INSTALLED_APPS
- ✅ **Pillow dependency** - Installed for ImageField support

## Step 3: Custom User Manager ✅

### **CustomUserManager** (`accounts/models.py`):
```python
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create and return a regular user with the given username, email, and password."""
        if not username:
            raise ValueError(_('The Username field must be set'))
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and return a superuser with the given username, email, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(username, email, password, **extra_fields)
```

### **Manager Features**:
- ✅ **create_user method** - Handles new fields correctly
- ✅ **create_superuser method** - Ensures admin users can be created
- ✅ **Email normalization** - Proper email handling
- ✅ **Field validation** - Username requirement validation
- ✅ **Permission defaults** - Proper staff/superuser flag handling

## Step 4: Django Admin Integration ✅

### **CustomUserAdmin** (`accounts/admin.py`):
```python
class CustomUserAdmin(UserAdmin):
    # Fields to display in the user list view
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'date_of_birth', 'is_staff', 'is_active', 'date_joined',
        'get_full_name', 'age'
    )
    
    # Fields that can be used for filtering
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'date_joined',
        'date_of_birth'
    )
    
    # Fieldsets for editing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
```

### **Admin Features**:
- ✅ **Enhanced list display** - Shows custom fields
- ✅ **Custom filtering** - Filter by date_of_birth
- ✅ **Organized fieldsets** - Logical grouping of fields
- ✅ **Custom methods** - Display full name and age
- ✅ **Add user form** - Includes custom fields
- ✅ **Search functionality** - Search by username, name, email

## Step 5: Application Updates ✅

### **Updated Models** (`relationship_app/models.py`):
```python
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class UserProfile(models.Model):
    # One-to-one relationship with custom user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
```

### **Application Integration**:
- ✅ **get_user_model()** - Dynamic user model reference
- ✅ **UserProfile compatibility** - Works with custom user
- ✅ **Foreign key updates** - All user references updated
- ✅ **Signal compatibility** - User creation signals work

## Database Migration ✅

### **Migration Process**:
- ✅ **Fresh database** - Created new database for custom user model
- ✅ **Migration files** - `accounts/migrations/0001_initial.py` created
- ✅ **All apps migrated** - All existing apps work with custom user
- ✅ **No data loss** - Clean migration process

### **Migration Commands**:
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

## Custom User Model Features

### **Additional Properties**:
```python
@property
def age(self):
    """Calculate and return the user's age based on date_of_birth."""
    if self.date_of_birth:
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    return None
```

### **Enhanced Methods**:
- ✅ **Age calculation** - Automatic age from birth date
- ✅ **Full name display** - Enhanced name formatting
- ✅ **String representation** - Clean user display
- ✅ **Short name method** - First name display

## Testing and Verification ✅

### **Verification Script** (`verify_custom_user.py`):
- ✅ **AUTH_USER_MODEL setting** - Correctly configured
- ✅ **Model class verification** - CustomUser properly loaded
- ✅ **Custom fields present** - date_of_birth and profile_photo
- ✅ **Custom manager active** - CustomUserManager in use
- ✅ **Method testing** - All custom methods working

### **Test Results**:
```
✅ AUTH_USER_MODEL setting: accounts.CustomUser
✅ CustomUser model class: <class 'accounts.models.CustomUser'>
✅ Custom fields added: date_of_birth, profile_photo
✅ Custom manager: CustomUserManager
✅ Model methods working correctly
```

## Security and Best Practices

### **Security Features**:
- ✅ **Password hashing** - Django's built-in security
- ✅ **Field validation** - Proper input validation
- ✅ **Permission inheritance** - All Django permissions work
- ✅ **Admin security** - Proper admin access controls

### **Best Practices Implemented**:
- ✅ **Internationalization** - gettext_lazy for translations
- ✅ **Help text** - User-friendly field descriptions
- ✅ **Null/blank handling** - Proper optional field configuration
- ✅ **Upload path** - Organized media file structure
- ✅ **Manager inheritance** - Proper BaseUserManager usage

## Conclusion

The custom user model implementation is complete and fully functional:

- ✅ **Custom User Model** - Extends AbstractUser with additional fields
- ✅ **Custom User Manager** - Handles user creation with new fields
- ✅ **Settings Configuration** - AUTH_USER_MODEL properly set
- ✅ **Admin Integration** - Full admin interface support
- ✅ **Application Updates** - All references updated to use custom user
- ✅ **Database Migration** - Clean migration to custom user model
- ✅ **Testing Verification** - All functionality verified working

The application now has a robust, extensible user model that can accommodate future requirements while maintaining full compatibility with Django's authentication system.
