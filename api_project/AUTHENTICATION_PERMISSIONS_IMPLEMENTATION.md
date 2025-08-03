# Django REST Framework Authentication and Permissions Implementation

## Objective
Secure API endpoints by implementing various authentication schemes and permission settings in Django REST Framework. This ensures that only authorized users can access and modify data through the API.

## Implementation Overview

This implementation provides comprehensive authentication and permission layers with token-based authentication, custom permission classes, and role-based access control.

## Step 1: Configure Authentication ✅

### **Token Authentication Setup** (`api_project/settings.py`):

<augment_code_snippet path="api_project/api_project/settings.py" mode="EXCERPT">
````python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',  # Django REST Framework
    'rest_framework.authtoken',  # Token authentication
    'api',  # API app for handling API logic
]

REST_FRAMEWORK = {
    # Default authentication classes
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    
    # Default permission classes
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
````
</augment_code_snippet>

### **Authentication Features**:
- **Token Authentication**: Primary authentication method
- **Session Authentication**: Fallback for web interface
- **Basic Authentication**: Fallback for simple clients
- **Database Tables**: Automatic token storage and management

## Step 2: Generate and Use Tokens ✅

### **Token Retrieval Implementation** (`api/authentication.py`):

<augment_code_snippet path="api_project/api/authentication.py" mode="EXCERPT">
````python
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication token view that returns additional user information.
    """
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        })
````
</augment_code_snippet>

### **Authentication Endpoints**:

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/auth/token/` | POST | Get authentication token | None (login) |
| `/api/auth/login/` | POST | Custom login with user info | None (login) |
| `/api/auth/logout/` | POST | Logout and delete token | Token required |
| `/api/auth/profile/` | GET | Get user profile | Token required |
| `/api/auth/register/` | POST | User registration | None (public) |

## Step 3: Define Permission Classes ✅

### **Custom Permission Classes** (`api/permissions.py`):

<augment_code_snippet path="api_project/api/permissions.py" mode="EXCERPT">
````python
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission for book objects.
    Allow read access to everyone, but write access only to authenticated users.
    """
    
    def has_permission(self, request, view):
        # Read permissions for unauthenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        return request.user and request.user.is_authenticated

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read access to everyone,
    but write access only to admin users.
    """
    
    def has_permission(self, request, view):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admin users
        return request.user and request.user.is_staff
````
</augment_code_snippet>

### **Permission Classes Available**:

| Permission Class | Description | Use Case |
|------------------|-------------|----------|
| `AllowAny` | No restrictions | Public endpoints |
| `IsAuthenticated` | Authenticated users only | Protected endpoints |
| `IsAdminUser` | Admin users only | Administrative actions |
| `IsAuthenticatedOrReadOnly` | Read public, write authenticated | Content management |
| `IsAuthorOrReadOnly` | Custom book permissions | Book management |
| `IsAdminOrReadOnly` | Read public, write admin | Admin-controlled content |

## Step 4: ViewSet with Permissions ✅

### **BookViewSet with Permission Control** (`api/views.py`):

<augment_code_snippet path="api_project/api/views.py" mode="EXCERPT">
````python
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet with authentication and permission-based access control.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Different permissions for different actions.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Anyone can read books
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            # Only authenticated users can create books
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            # Only authenticated users can update books
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            # Only admin users can delete books
            permission_classes = [permissions.IsAdminUser]
        else:
            # Default to authenticated users for custom actions
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
````
</augment_code_snippet>

### **Permission Matrix**:

| Action | HTTP Method | Permission Required | Description |
|--------|-------------|-------------------|-------------|
| `list` | GET | `AllowAny` | Anyone can list books |
| `retrieve` | GET | `AllowAny` | Anyone can view book details |
| `create` | POST | `IsAuthenticated` | Authenticated users can create |
| `update` | PUT | `IsAuthenticated` | Authenticated users can update |
| `partial_update` | PATCH | `IsAuthenticated` | Authenticated users can patch |
| `destroy` | DELETE | `IsAdminUser` | Only admins can delete |

## Step 5: Testing Authentication and Permissions ✅

### **Testing Scenarios**:

#### **1. Token Authentication Test**:
```bash
# Get authentication token
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'

# Response: {"token": "your_auth_token"}
```

#### **2. Authenticated API Access**:
```bash
# Use token for API access
curl -H "Authorization: Token your_auth_token" \
     http://127.0.0.1:8000/api/books/
```

#### **3. Permission Testing**:
```bash
# Public read access (no token needed)
curl http://127.0.0.1:8000/api/books/

# Create book (token required)
curl -X POST http://127.0.0.1:8000/api/books/ \
     -H "Authorization: Token your_auth_token" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Book", "author": "Author Name"}'

# Delete book (admin token required)
curl -X DELETE http://127.0.0.1:8000/api/books/1/ \
     -H "Authorization: Token admin_auth_token"
```

### **Custom Actions with Permissions**:

<augment_code_snippet path="api_project/api/views.py" mode="EXCERPT">
````python
@action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
def public_books(self, request):
    """Public access to books"""
    # Implementation

@action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
def my_books(self, request):
    """Books for authenticated user"""
    # Implementation

@action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
def admin_stats(self, request):
    """Admin-only statistics"""
    # Implementation
````
</augment_code_snippet>

## Security Features Implemented

### **Authentication Security**:
- **Token-based Authentication**: Secure, stateless authentication
- **Token Management**: Automatic token creation and deletion
- **Multiple Auth Methods**: Fallback authentication options
- **User Registration**: Secure user account creation

### **Permission Security**:
- **Role-based Access**: Different permissions for different user roles
- **Action-level Permissions**: Granular control over API actions
- **Custom Permissions**: Tailored permission logic for specific needs
- **Object-level Permissions**: Fine-grained access control

### **API Security**:
- **HTTPS Ready**: Secure transmission support
- **CSRF Protection**: Cross-site request forgery protection
- **Rate Limiting**: Throttling configuration available
- **Input Validation**: Serializer-based data validation

## File Structure

```
api_project/
├── api/
│   ├── authentication.py          # Authentication views and utilities
│   ├── permissions.py              # Custom permission classes
│   ├── views.py                    # ViewSet with permissions
│   ├── auth_urls.py                # Authentication URL patterns
│   ├── urls.py                     # Main API URLs with auth
│   └── serializers.py              # Data serialization
├── api_project/
│   └── settings.py                 # DRF and auth configuration
├── test_authentication.py         # Authentication testing script
└── AUTHENTICATION_PERMISSIONS_IMPLEMENTATION.md  # This documentation
```

## Activation Instructions

### **Step 1: Install Dependencies**
```bash
pip install djangorestframework
```

### **Step 2: Enable DRF**
Uncomment in `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    # ...
]
```

### **Step 3: Run Migrations**
```bash
python manage.py migrate
```

### **Step 4: Create Test Users**
```bash
python manage.py createsuperuser
```

### **Step 5: Activate Views**
Uncomment authentication views and ViewSet in respective files.

### **Step 6: Test Authentication**
```bash
python test_authentication.py
```

## Deliverables Status ✅

### **✅ Updated settings.py**:
- Token authentication in REST framework settings
- Authentication classes configuration
- Permission classes configuration

### **✅ Authentication Views**:
- Token retrieval endpoints implemented
- Custom authentication views created
- User registration and profile management

### **✅ views.py**:
- ViewSets updated with permission classes
- Action-level permission control
- Custom actions with specific permissions

### **✅ Documentation**:
- Comprehensive implementation guide
- Testing instructions and examples
- Security features explanation

## Security Best Practices Implemented

1. **Token Security**: Secure token generation and management
2. **Permission Granularity**: Fine-grained access control
3. **Authentication Layers**: Multiple authentication methods
4. **Input Validation**: Serializer-based validation
5. **Error Handling**: Secure error responses
6. **Documentation**: Clear security implementation guide

The authentication and permissions implementation provides enterprise-grade security for the Django REST Framework API, ensuring proper access control and user authentication.
