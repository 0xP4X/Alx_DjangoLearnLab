#!/usr/bin/env python
"""
Script to test the custom user model functionality
"""
import os
import sys
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from accounts.models import CustomUser

def test_custom_user_model():
    """Test the custom user model functionality"""
    
    print("Testing Custom User Model...")
    
    # Test creating a regular user
    print("\n1. Creating a regular user...")
    user = CustomUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        date_of_birth=date(1990, 5, 15)
    )
    print(f"Created user: {user.username}")
    print(f"Full name: {user.get_full_name()}")
    print(f"Age: {user.age}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is superuser: {user.is_superuser}")
    
    # Test creating a superuser
    print("\n2. Creating a superuser...")
    try:
        admin_user = CustomUser.objects.create_superuser(
            username='superadmin',
            email='superadmin@example.com',
            password='admin123',
            first_name='Super',
            last_name='Admin',
            date_of_birth=date(1985, 1, 1)
        )
    except Exception as e:
        print(f"Superuser might already exist, getting existing one: {e}")
        admin_user = CustomUser.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = CustomUser.objects.create_superuser(
                username='superadmin2',
                email='superadmin2@example.com',
                password='admin123'
            )
    print(f"Created superuser: {admin_user.username}")
    print(f"Full name: {admin_user.get_full_name()}")
    print(f"Age: {admin_user.age}")
    print(f"Is staff: {admin_user.is_staff}")
    print(f"Is superuser: {admin_user.is_superuser}")
    
    # Test user model methods
    print("\n3. Testing user model methods...")
    print(f"User string representation: {str(user)}")
    print(f"User short name: {user.get_short_name()}")
    
    # Display all users
    print(f"\n4. All users in database:")
    for u in CustomUser.objects.all():
        print(f"- {u.username} ({u.get_full_name()}) - Age: {u.age}")
    
    print("\nCustom User Model test completed successfully!")

if __name__ == '__main__':
    test_custom_user_model()
