# Django Security Implementation Guide

## Objective
Apply best practices for securing a Django application by implementing comprehensive security measures to protect against common vulnerabilities such as cross-site scripting (XSS), cross-site request forgery (CSRF), and SQL injection.

## Security Implementation Overview

This implementation demonstrates production-ready security practices for Django applications, covering configuration, code security, and monitoring.

## Step 1: Secure Settings Configuration ✅

### **Security Settings Implemented** (`LibraryProject/settings.py`):

#### **Debug and Host Configuration**:
```python
# Set DEBUG to False in production to prevent information disclosure
DEBUG = True  # Set to False in production

# Configure allowed hosts for production security
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Add your production domains
```

#### **HTTPS and Cookie Security**:
```python
# Enforce HTTPS for cookies - prevents cookie theft over insecure connections
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS

# Additional cookie security settings
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
CSRF_COOKIE_SAMESITE = 'Strict'  # Prevent CSRF attacks via cross-site requests
SESSION_COOKIE_SAMESITE = 'Strict'  # Prevent session hijacking
```

#### **Browser Security Headers**:
```python
# Enable browser's built-in XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Prevent MIME type sniffing which can lead to security vulnerabilities
SECURE_CONTENT_TYPE_NOSNIFF = True

# Prevent the site from being embedded in frames (clickjacking protection)
X_FRAME_OPTIONS = 'DENY'
```

#### **Password Security**:
```python
# Use strong password hashers (Argon2 is recommended)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Enhanced password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'max_similarity': 0.7}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}  # Require minimum 12 characters
    },
    # ... additional validators
]
```

## Step 2: CSRF Protection Implementation ✅

### **Template CSRF Tokens**:

All forms include CSRF protection:

```html
<!-- book_form.html -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>

<!-- book_confirm_delete.html -->
<form method="post">
    {% csrf_token %}
    <!-- confirmation content -->
</form>
```

### **View-Level CSRF Protection**:
```python
@csrf_protect
def book_create(request):
    """CSRF protection enforced at view level"""
    # view implementation
```

## Step 3: Secure Data Access and Input Validation ✅

### **Secure Forms Implementation** (`bookshelf/forms.py`):

#### **SecureBookForm Features**:
- **Input Validation**: Custom validators for title and author fields
- **XSS Prevention**: HTML tag stripping and content sanitization
- **Length Validation**: Enforced minimum and maximum lengths
- **Pattern Validation**: Regex validation for allowed characters
- **Injection Prevention**: Detection of malicious patterns

```python
def clean_title(self):
    """Custom validation and sanitization for title field"""
    title = self.cleaned_data.get('title')
    
    # Strip HTML tags to prevent XSS
    title = strip_tags(title).strip()
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'<script.*?>.*?</script>',  # Script tags
        r'javascript:',              # JavaScript protocol
        r'on\w+\s*=',               # Event handlers
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            raise ValidationError('Title contains potentially malicious content.')
    
    return title
```

### **Secure Views Implementation** (`bookshelf/views.py`):

#### **SQL Injection Prevention**:
```python
# Use Django ORM for secure database queries (prevents SQL injection)
if search_type == 'title':
    books = books.filter(title__icontains=query)
elif search_type == 'author':
    books = books.filter(author__icontains=query)
else:  # both
    books = books.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )
```

#### **Input Validation and Sanitization**:
```python
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
@never_cache
def book_list(request):
    """Secure view with comprehensive input validation"""
    
    # Handle secure search functionality
    if request.method == 'GET' and 'query' in request.GET:
        search_form = SecureSearchForm(request.GET)
        if search_form.is_valid():
            # Use validated and sanitized data
            query = search_form.cleaned_data['query']
            # ... secure database operations
```

#### **Security Logging**:
```python
# Log search activity for security monitoring
logger.info(f'User {request.user.username} searched for: {query}')

# Log invalid search attempts
logger.warning(f'Invalid search attempt by user {request.user.username}: {request.GET}')
```

## Step 4: Content Security Policy (CSP) Implementation ✅

### **CSP Middleware** (`bookshelf/middleware.py`):

#### **SecurityHeadersMiddleware Features**:
- **Content Security Policy**: Restricts resource loading domains
- **XSS Protection**: Additional browser-side XSS prevention
- **Clickjacking Protection**: Frame embedding restrictions
- **MIME Type Protection**: Prevents MIME sniffing attacks

```python
def process_response(self, request, response):
    """Add security headers to all responses"""
    
    # Content Security Policy (CSP) Header
    csp_directives = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline'",  # Restrict in production
        "style-src 'self' 'unsafe-inline'",   # Restrict in production
        "img-src 'self' data: https:",
        "font-src 'self' https:",
        "connect-src 'self'",
        "frame-ancestors 'none'",  # Prevent framing
        "base-uri 'self'",
        "form-action 'self'",
        "upgrade-insecure-requests",
    ]
    
    response['Content-Security-Policy'] = "; ".join(csp_directives)
```

#### **Additional Security Headers**:
- **X-Content-Type-Options**: `nosniff`
- **X-XSS-Protection**: `1; mode=block`
- **Referrer-Policy**: `strict-origin-when-cross-origin`
- **Permissions-Policy**: Restricts browser features

### **Security Logging Middleware**:
- **Suspicious Pattern Detection**: Monitors for malicious content
- **Failed Authentication Logging**: Tracks 403 responses
- **Server Error Monitoring**: Logs potential attack indicators

### **Rate Limiting Middleware**:
- **IP-based Rate Limiting**: Prevents abuse and DoS attacks
- **Configurable Limits**: 100 requests per minute per IP
- **Automatic Cleanup**: Removes old rate limit data

## Security Features Summary

### **Protection Against Common Vulnerabilities**:

#### **Cross-Site Scripting (XSS)**:
- ✅ **Template Auto-escaping**: Django's built-in XSS protection
- ✅ **Content Security Policy**: Restricts script execution
- ✅ **Input Sanitization**: HTML tag stripping in forms
- ✅ **XSS Protection Headers**: Browser-side XSS filtering

#### **Cross-Site Request Forgery (CSRF)**:
- ✅ **CSRF Tokens**: All forms include `{% csrf_token %}`
- ✅ **CSRF Middleware**: Automatic token validation
- ✅ **Secure Cookies**: CSRF cookies with security flags
- ✅ **SameSite Cookies**: Prevents cross-site cookie usage

#### **SQL Injection**:
- ✅ **Django ORM**: Parameterized queries prevent injection
- ✅ **Input Validation**: Form validation and sanitization
- ✅ **Pattern Detection**: Monitors for SQL injection attempts
- ✅ **Secure Search**: Validated search parameters

#### **Clickjacking**:
- ✅ **X-Frame-Options**: Prevents iframe embedding
- ✅ **CSP Frame Ancestors**: Additional frame protection
- ✅ **Middleware Protection**: Automatic header injection

#### **Session Security**:
- ✅ **Secure Session Cookies**: HTTPS-only in production
- ✅ **HttpOnly Cookies**: Prevents JavaScript access
- ✅ **Session Timeout**: Automatic session expiration
- ✅ **SameSite Protection**: Cross-site session protection

## File Structure

```
LibraryProject/
├── LibraryProject/
│   └── settings.py                 # Comprehensive security settings
├── bookshelf/
│   ├── forms.py                    # Secure form validation
│   ├── views.py                    # Security-enhanced views
│   ├── middleware.py               # CSP and security middleware
│   └── templates/bookshelf/
│       ├── book_list.html          # CSRF-protected templates
│       ├── book_form.html          # Secure form implementation
│       ├── book_confirm_delete.html # CSRF-protected deletion
│       └── form_example.html       # Security demonstration
├── logs/
│   └── security.log                # Security event logging
└── SECURITY_IMPLEMENTATION_GUIDE.md # This documentation
```

## Testing and Verification

### **Security Testing Approach**:

#### **Manual Testing**:
1. **CSRF Protection**: Attempt form submissions without CSRF tokens
2. **XSS Prevention**: Test input fields with script tags
3. **SQL Injection**: Test search with SQL injection patterns
4. **Permission Enforcement**: Access restricted views without permissions
5. **Rate Limiting**: Exceed request limits to test throttling

#### **Security Headers Verification**:
```bash
# Check security headers
curl -I http://127.0.0.1:8000/bookshelf/

# Expected headers:
# Content-Security-Policy: default-src 'self'; ...
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# X-Frame-Options: DENY
```

#### **Form Security Testing**:
- Test forms with malicious input
- Verify CSRF token validation
- Check input sanitization
- Validate error handling

## Production Deployment Checklist

### **Critical Security Settings for Production**:
```python
# settings.py for production
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### **Additional Production Considerations**:
- Use environment variables for sensitive settings
- Implement proper logging and monitoring
- Regular security updates and patches
- SSL/TLS certificate configuration
- Database connection encryption
- Backup and recovery procedures

## Conclusion

This implementation provides comprehensive security coverage including:

- ✅ **Secure Settings Configuration**: Production-ready security settings
- ✅ **CSRF Protection**: Complete form and view protection
- ✅ **Input Validation**: Comprehensive form validation and sanitization
- ✅ **Content Security Policy**: XSS prevention via CSP headers
- ✅ **Security Monitoring**: Logging and rate limiting
- ✅ **Best Practices**: Following Django security recommendations

The application is now protected against common web vulnerabilities and follows industry security standards.

## Security Testing Commands

### **Setup and Testing**:
```bash
# Run migrations
python manage.py migrate

# Create test users (if not already created)
python manage.py create_test_users

# Start development server
python manage.py runserver

# Test security implementation
python test_security.py
```

### **Manual Security Testing**:
1. **Visit**: `http://127.0.0.1:8000/bookshelf/`
2. **Test CSRF**: Try form submissions without tokens
3. **Test XSS**: Input `<script>alert('XSS')</script>` in forms
4. **Test SQL Injection**: Search for `'; DROP TABLE books; --`
5. **Test Permissions**: Access restricted URLs without proper permissions
