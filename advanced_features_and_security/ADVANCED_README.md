# Advanced Features and Security

This directory contains Django projects demonstrating advanced features and security implementations, including custom user models and enhanced authentication systems.

## Projects

### LibraryProject (Advanced Features)
A Django application demonstrating:
- **Custom User Model**: Extended AbstractUser with additional fields
- **Custom User Manager**: Handles user creation with new fields
- **Role-Based Access Control**: Admin, Librarian, Member roles
- **Custom Permissions**: Granular book management permissions
- **Enhanced Authentication**: Login, logout, registration with custom user
- **Django Admin Integration**: Full admin support for custom user model
- **Security Features**: Permission-based access control

## Key Features Implemented

### 🔐 Custom User Model
- **CustomUser**: Extends AbstractUser with `date_of_birth` and `profile_photo` fields
- **CustomUserManager**: Handles user creation and management
- **Age Calculation**: Automatic age property from birth date
- **Profile Photos**: ImageField support with Pillow

### 🛡️ Authentication & Authorization
- **Role-Based Access**: Three-tier system (Admin > Librarian > Member)
- **Custom Permissions**: Book add, change, delete permissions
- **Permission Decorators**: `@permission_required` on views
- **User Profiles**: Extended user information with roles

### 📱 Enhanced User Interface
- **Role-Specific Dashboards**: Tailored views for each user role
- **Permission-Aware Templates**: Conditional display based on permissions
- **CRUD Operations**: Full book management with security
- **Responsive Design**: Professional styling across all templates

### 🔒 Security Implementation
- **Permission-Based Access Control**: Granular permission system
- **Django's Built-in Security**: Password hashing, CSRF protection
- **User Authentication**: Secure login/logout/registration
- **Admin Interface**: Enhanced admin with custom user fields

## Setup Instructions

1. **Navigate to the project directory**
   ```bash
   cd advanced_features_and_security/LibraryProject
   ```

2. **Install dependencies**
   ```bash
   pip install django Pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Test the custom user model**
   ```bash
   python verify_custom_user.py
   ```

## File Structure

```
advanced_features_and_security/LibraryProject/
├── accounts/                           # Custom user model app
│   ├── models.py                      # CustomUser and CustomUserManager
│   ├── admin.py                       # CustomUserAdmin configuration
│   └── migrations/                    # Database migrations
├── relationship_app/                  # Main application
│   ├── models.py                      # Updated to use custom user
│   ├── views.py                       # Role-based and permission views
│   ├── urls.py                        # URL routing
│   └── templates/                     # Enhanced templates
├── LibraryProject/
│   └── settings.py                    # AUTH_USER_MODEL configuration
├── custom_user_model_documentation.md # Complete implementation guide
├── verify_custom_user.py              # Testing script
└── test_custom_user.py                # User creation testing
```

## Learning Objectives

- **Custom User Models**: Extending Django's authentication system
- **User Management**: Custom managers and user creation
- **Permission Systems**: Role-based and permission-based access control
- **Security Best Practices**: Django security features and implementations
- **Admin Customization**: Enhancing Django admin for custom models
- **Template Security**: Permission-aware user interfaces
- **Database Design**: Advanced user model relationships

## Testing

### Verification Script
Run the verification script to test all custom user model functionality:
```bash
python verify_custom_user.py
```

### Test Users
The system includes test users for each role:
- **Admin**: Full system access
- **Librarian**: Book management access
- **Member**: Read-only access

### Permission Testing
Test permission-based access by logging in with different user roles and attempting various operations.

## Documentation

- **`custom_user_model_documentation.md`**: Complete implementation guide
- **`role_based_access_documentation.md`**: Role-based access control details
- **`custom_permissions_documentation.md`**: Permission system documentation
- **`authentication_documentation.md`**: Authentication system overview

## Advanced Features

This project demonstrates production-ready Django features including:
- Custom user models for scalable applications
- Comprehensive permission systems
- Role-based access control
- Security best practices
- Professional admin interfaces
- Extensible authentication systems

Perfect for learning advanced Django development and security implementation!
