"""
Authentication URL patterns for the API app.
This module contains URL patterns for authentication endpoints.
"""

from django.urls import path
from . import authentication
# from rest_framework.authtoken.views import obtain_auth_token

# Authentication URL patterns (ready for DRF activation)
urlpatterns = [
    # Basic authentication info (current)
    path('', authentication.auth_info_view, name='auth_info'),
    path('basic-login/', authentication.basic_login_view, name='basic_login'),
    
    # Django REST Framework authentication endpoints (uncomment after DRF installation)
    # Built-in token authentication
    # path('token/', obtain_auth_token, name='api_token_auth'),
    
    # Custom authentication views
    # path('login/', authentication.CustomAuthToken.as_view(), name='api_login'),
    # path('logout/', authentication.logout_view, name='api_logout'),
    # path('profile/', authentication.user_profile_view, name='api_profile'),
    # path('register/', authentication.register_view, name='api_register'),
    
    # Alternative login endpoint
    # path('auth/', authentication.login_view, name='api_auth'),
]

# URL patterns that will be available after DRF activation:
"""
Authentication Endpoints:

1. Token Authentication (Built-in):
   POST /api/auth/token/
   {
       "username": "your_username",
       "password": "your_password"
   }
   Returns: {"token": "your_auth_token"}

2. Custom Login:
   POST /api/auth/login/
   {
       "username": "your_username", 
       "password": "your_password"
   }
   Returns: {"token": "token", "user": {user_details}}

3. Logout:
   POST /api/auth/logout/
   Headers: Authorization: Token your_auth_token
   Returns: {"message": "Successfully logged out"}

4. User Profile:
   GET /api/auth/profile/
   Headers: Authorization: Token your_auth_token
   Returns: {user_profile_data}

5. User Registration:
   POST /api/auth/register/
   {
       "username": "new_username",
       "password": "new_password",
       "email": "user@example.com",
       "first_name": "First",
       "last_name": "Last"
   }
   Returns: {"token": "new_token", "user": {user_details}}

Usage Examples:

1. Get Token:
   curl -X POST http://127.0.0.1:8000/api/auth/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "password"}'

2. Use Token for API Access:
   curl -H "Authorization: Token your_auth_token" \
        http://127.0.0.1:8000/api/books/

3. Create Book with Authentication:
   curl -X POST http://127.0.0.1:8000/api/books/ \
        -H "Authorization: Token your_auth_token" \
        -H "Content-Type: application/json" \
        -d '{"title": "New Book", "author": "Author Name"}'
"""
