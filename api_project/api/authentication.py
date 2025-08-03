"""
Django REST Framework Authentication Views and Utilities
This module provides authentication views and utilities for token-based authentication.
"""

# from django.contrib.auth import authenticate
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken import views as auth_views
# from django.contrib.auth.models import User


# class CustomAuthToken(ObtainAuthToken):
#     """
#     Custom authentication token view that returns additional user information.
#     Extends the default ObtainAuthToken to provide more user details.
#     """
#     
#     def post(self, request, *args, **kwargs):
#         """
#         Handle POST request for token authentication.
#         Returns token along with user information.
#         """
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'username': user.username,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'is_staff': user.is_staff,
#             'is_superuser': user.is_superuser,
#             'date_joined': user.date_joined,
#             'last_login': user.last_login,
#         })


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     """
#     Login view that returns authentication token.
#     
#     POST /api/auth/login/
#     {
#         "username": "your_username",
#         "password": "your_password"
#     }
#     
#     Returns:
#     {
#         "token": "your_auth_token",
#         "user": {user_details}
#     }
#     """
#     username = request.data.get('username')
#     password = request.data.get('password')
#     
#     if username and password:
#         user = authenticate(username=username, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'token': token.key,
#                 'user': {
#                     'id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                     'is_staff': user.is_staff,
#                 }
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 'error': 'Invalid credentials'
#             }, status=status.HTTP_401_UNAUTHORIZED)
#     else:
#         return Response({
#             'error': 'Username and password required'
#         }, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def logout_view(request):
#     """
#     Logout view that deletes the authentication token.
#     
#     POST /api/auth/logout/
#     Headers: Authorization: Token your_auth_token
#     
#     Returns:
#     {
#         "message": "Successfully logged out"
#     }
#     """
#     try:
#         # Delete the user's token to logout
#         request.user.auth_token.delete()
#         return Response({
#             'message': 'Successfully logged out'
#         }, status=status.HTTP_200_OK)
#     except:
#         return Response({
#             'error': 'Error logging out'
#         }, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def user_profile_view(request):
#     """
#     Get current user profile information.
#     
#     GET /api/auth/profile/
#     Headers: Authorization: Token your_auth_token
#     
#     Returns user profile information.
#     """
#     user = request.user
#     return Response({
#         'id': user.id,
#         'username': user.username,
#         'email': user.email,
#         'first_name': user.first_name,
#         'last_name': user.last_name,
#         'is_staff': user.is_staff,
#         'is_superuser': user.is_superuser,
#         'date_joined': user.date_joined,
#         'last_login': user.last_login,
#     })


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_view(request):
#     """
#     User registration view.
#     
#     POST /api/auth/register/
#     {
#         "username": "new_username",
#         "password": "new_password",
#         "email": "user@example.com",
#         "first_name": "First",
#         "last_name": "Last"
#     }
#     
#     Returns:
#     {
#         "token": "new_auth_token",
#         "user": {user_details}
#     }
#     """
#     username = request.data.get('username')
#     password = request.data.get('password')
#     email = request.data.get('email', '')
#     first_name = request.data.get('first_name', '')
#     last_name = request.data.get('last_name', '')
#     
#     if not username or not password:
#         return Response({
#             'error': 'Username and password are required'
#         }, status=status.HTTP_400_BAD_REQUEST)
#     
#     if User.objects.filter(username=username).exists():
#         return Response({
#             'error': 'Username already exists'
#         }, status=status.HTTP_400_BAD_REQUEST)
#     
#     # Create new user
#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email,
#         first_name=first_name,
#         last_name=last_name
#     )
#     
#     # Create token for new user
#     token = Token.objects.create(user=user)
#     
#     return Response({
#         'token': token.key,
#         'user': {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#         }
#     }, status=status.HTTP_201_CREATED)


# Temporary basic authentication views (without DRF)
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["POST"])
def basic_login_view(request):
    """
    Basic login view without DRF (temporary implementation).
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                return JsonResponse({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                    },
                    'note': 'Install DRF for token authentication'
                })
            else:
                return JsonResponse({
                    'error': 'Invalid credentials'
                }, status=401)
        else:
            return JsonResponse({
                'error': 'Username and password required'
            }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON'
        }, status=400)


def auth_info_view(request):
    """
    Authentication information view.
    """
    return JsonResponse({
        'message': 'Django REST Framework Authentication Setup',
        'status': 'Ready for DRF installation',
        'authentication_methods': [
            'Token Authentication (after DRF installation)',
            'Session Authentication',
            'Basic Authentication'
        ],
        'endpoints': {
            'login': '/api/auth/login/',
            'logout': '/api/auth/logout/',
            'profile': '/api/auth/profile/',
            'register': '/api/auth/register/',
            'token': '/api/auth/token/',
        },
        'installation_steps': [
            'pip install djangorestframework',
            'Uncomment rest_framework in INSTALLED_APPS',
            'Run python manage.py migrate',
            'Uncomment authentication views',
            'Test with token authentication'
        ]
    }, json_dumps_params={'indent': 2})
