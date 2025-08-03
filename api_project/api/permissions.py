"""
Django REST Framework Custom Permission Classes
This module defines custom permission classes for API access control.
"""

# from rest_framework import permissions


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     Read permissions are allowed for any request,
#     Write permissions are only allowed to the owner of the object.
#     """
#     
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         
#         # Write permissions are only allowed to the owner of the object.
#         return obj.owner == request.user


# class IsAuthorOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission for book objects.
#     Allow read access to everyone, but write access only to authenticated users.
#     For future use when books have an author field linked to users.
#     """
#     
#     def has_permission(self, request, view):
#         # Read permissions for unauthenticated users
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         
#         # Write permissions require authentication
#         return request.user and request.user.is_authenticated
#     
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         
#         # Write permissions are only allowed to the author of the book
#         # (This would require adding an author field to the Book model)
#         # return obj.author == request.user
#         
#         # For now, allow any authenticated user to edit
#         return request.user and request.user.is_authenticated


# class IsAdminOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to allow read access to everyone,
#     but write access only to admin users.
#     """
#     
#     def has_permission(self, request, view):
#         # Read permissions for everyone
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         
#         # Write permissions only for admin users
#         return request.user and request.user.is_staff


# class IsAuthenticatedOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to allow read access to everyone,
#     but write access only to authenticated users.
#     """
#     
#     def has_permission(self, request, view):
#         # Read permissions for everyone
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         
#         # Write permissions only for authenticated users
#         return request.user and request.user.is_authenticated


# class IsSuperUserOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to allow read access to everyone,
#     but write access only to superusers.
#     """
#     
#     def has_permission(self, request, view):
#         # Read permissions for everyone
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         
#         # Write permissions only for superusers
#         return request.user and request.user.is_superuser


# class IsOwnerOrAdmin(permissions.BasePermission):
#     """
#     Custom permission to allow access to owners or admin users.
#     """
#     
#     def has_object_permission(self, request, view, obj):
#         # Allow access to the owner or admin users
#         return (
#             obj.owner == request.user or 
#             request.user.is_staff or 
#             request.user.is_superuser
#         )


# class CanCreateBooks(permissions.BasePermission):
#     """
#     Custom permission for creating books.
#     Only authenticated users with specific permissions can create books.
#     """
#     
#     def has_permission(self, request, view):
#         if request.method == 'POST':
#             # Check if user is authenticated and has permission to add books
#             return (
#                 request.user and 
#                 request.user.is_authenticated and
#                 (request.user.is_staff or request.user.has_perm('api.add_book'))
#             )
#         return True


# class CanDeleteBooks(permissions.BasePermission):
#     """
#     Custom permission for deleting books.
#     Only admin users can delete books.
#     """
#     
#     def has_permission(self, request, view):
#         if request.method == 'DELETE':
#             return request.user and request.user.is_staff
#         return True


# Permission combinations for different use cases:

# PERMISSION_SETS = {
#     'public_read_auth_write': [
#         permissions.IsAuthenticatedOrReadOnly,
#     ],
#     'admin_only': [
#         permissions.IsAdminUser,
#     ],
#     'authenticated_only': [
#         permissions.IsAuthenticated,
#     ],
#     'owner_or_admin': [
#         IsOwnerOrAdmin,
#     ],
#     'admin_or_read_only': [
#         IsAdminOrReadOnly,
#     ],
#     'superuser_or_read_only': [
#         IsSuperUserOrReadOnly,
#     ],
# }


# Example usage in ViewSets:
"""
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        '''
        Instantiates and returns the list of permissions that this view requires.
        '''
        if self.action == 'list' or self.action == 'retrieve':
            # Anyone can read books
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            # Only authenticated users can create books
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            # Only the author or admin can update books
            permission_classes = [IsAuthorOrReadOnly]
        elif self.action == 'destroy':
            # Only admin can delete books
            permission_classes = [permissions.IsAdminUser]
        else:
            # Default to authenticated users
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
"""


# Temporary permission documentation (without DRF)
def get_permission_info():
    """
    Returns information about available permission classes.
    """
    return {
        'message': 'Django REST Framework Permission Classes',
        'status': 'Ready for DRF installation',
        'built_in_permissions': {
            'AllowAny': 'Allow unrestricted access',
            'IsAuthenticated': 'Allow access only to authenticated users',
            'IsAdminUser': 'Allow access only to admin users',
            'IsAuthenticatedOrReadOnly': 'Read access for everyone, write access for authenticated users'
        },
        'custom_permissions': {
            'IsOwnerOrReadOnly': 'Read access for everyone, write access for owners',
            'IsAuthorOrReadOnly': 'Read access for everyone, write access for authors',
            'IsAdminOrReadOnly': 'Read access for everyone, write access for admins',
            'IsSuperUserOrReadOnly': 'Read access for everyone, write access for superusers',
            'CanCreateBooks': 'Permission to create books',
            'CanDeleteBooks': 'Permission to delete books'
        },
        'usage_examples': {
            'view_level': 'permission_classes = [IsAuthenticated]',
            'method_level': 'Use get_permissions() method for different actions',
            'object_level': 'Use has_object_permission() for specific objects'
        },
        'installation_note': 'Install DRF to activate permission classes'
    }
