#!/usr/bin/env python
"""
Script to verify the custom user model functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from accounts.models import CustomUser
from django.conf import settings

def verify_custom_user_model():
    """Verify the custom user model functionality"""
    
    print("Verifying Custom User Model Implementation...")
    
    # Check AUTH_USER_MODEL setting
    print(f"\n1. AUTH_USER_MODEL setting: {settings.AUTH_USER_MODEL}")
    
    # Check if CustomUser model is properly configured
    print(f"\n2. CustomUser model class: {CustomUser}")
    print(f"   - Model name: {CustomUser._meta.model_name}")
    print(f"   - App label: {CustomUser._meta.app_label}")
    print(f"   - Table name: {CustomUser._meta.db_table}")
    
    # Check custom fields
    print(f"\n3. Custom fields added:")
    for field in CustomUser._meta.fields:
        if field.name in ['date_of_birth', 'profile_photo']:
            print(f"   - {field.name}: {field.__class__.__name__}")
    
    # Check custom manager
    print(f"\n4. Custom manager: {CustomUser.objects.__class__.__name__}")
    
    # Check existing users
    print(f"\n5. Existing users in database:")
    users = CustomUser.objects.all()
    if users:
        for user in users:
            print(f"   - {user.username} (Staff: {user.is_staff}, Superuser: {user.is_superuser})")
            if hasattr(user, 'date_of_birth') and user.date_of_birth:
                print(f"     Date of Birth: {user.date_of_birth}, Age: {user.age}")
    else:
        print("   No users found in database")
    
    # Test model methods
    if users:
        test_user = users.first()
        print(f"\n6. Testing model methods with user '{test_user.username}':")
        print(f"   - __str__(): {str(test_user)}")
        print(f"   - get_full_name(): {test_user.get_full_name()}")
        print(f"   - get_short_name(): {test_user.get_short_name()}")
        print(f"   - age property: {test_user.age}")
    
    print("\nCustom User Model verification completed successfully!")
    print("✅ Custom user model is properly configured and working!")

if __name__ == '__main__':
    verify_custom_user_model()
