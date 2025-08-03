#!/usr/bin/env python
"""
Script to set up custom permissions for the Book model
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, UserProfile

def setup_permissions():
    """Set up custom permissions for users based on their roles"""
    
    # Get the custom permissions
    content_type = ContentType.objects.get_for_model(Book)
    can_add_book = Permission.objects.get(content_type=content_type, codename='can_add_book')
    can_change_book = Permission.objects.get(content_type=content_type, codename='can_change_book')
    can_delete_book = Permission.objects.get(content_type=content_type, codename='can_delete_book')

    print('Custom permissions found:')
    print(f'- {can_add_book.name} ({can_add_book.codename})')
    print(f'- {can_change_book.name} ({can_change_book.codename})')
    print(f'- {can_delete_book.name} ({can_delete_book.codename})')

    # Get existing users
    admin_user = User.objects.get(username='admin_user')
    librarian_user = User.objects.get(username='librarian_user')
    member_user = User.objects.get(username='member_user')

    # Clear existing permissions first
    admin_user.user_permissions.clear()
    librarian_user.user_permissions.clear()
    member_user.user_permissions.clear()

    # Admin gets all permissions
    admin_user.user_permissions.add(can_add_book, can_change_book, can_delete_book)
    print(f'\nAdmin user ({admin_user.username}) granted all book permissions')

    # Librarian gets add and change permissions
    librarian_user.user_permissions.add(can_add_book, can_change_book)
    print(f'Librarian user ({librarian_user.username}) granted add and change permissions')

    # Member gets no special permissions (read-only)
    print(f'Member user ({member_user.username}) has read-only access')

    # Verify permissions
    print(f'\nPermission verification:')
    print(f'Admin can add books: {admin_user.has_perm("relationship_app.can_add_book")}')
    print(f'Admin can change books: {admin_user.has_perm("relationship_app.can_change_book")}')
    print(f'Admin can delete books: {admin_user.has_perm("relationship_app.can_delete_book")}')

    print(f'\nLibrarian can add books: {librarian_user.has_perm("relationship_app.can_add_book")}')
    print(f'Librarian can change books: {librarian_user.has_perm("relationship_app.can_change_book")}')
    print(f'Librarian can delete books: {librarian_user.has_perm("relationship_app.can_delete_book")}')

    print(f'\nMember can add books: {member_user.has_perm("relationship_app.can_add_book")}')
    print(f'Member can change books: {member_user.has_perm("relationship_app.can_change_book")}')
    print(f'Member can delete books: {member_user.has_perm("relationship_app.can_delete_book")}')

    print('\nCustom permissions system setup completed!')

if __name__ == '__main__':
    setup_permissions()
