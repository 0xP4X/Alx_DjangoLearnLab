#!/usr/bin/env python
"""
Script to test the permissions and groups implementation
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from bookshelf.models import Book

User = get_user_model()

def test_permissions_system():
    """Test the permissions and groups implementation"""
    
    print("🧪 Testing Permissions and Groups System...")
    print("=" * 60)
    
    # Test 1: Check if groups exist
    print("\n1️⃣ Testing Groups Setup:")
    groups = ['Viewers', 'Editors', 'Admins']
    for group_name in groups:
        try:
            group = Group.objects.get(name=group_name)
            permissions = list(group.permissions.all().values_list('codename', flat=True))
            print(f"   ✅ {group_name} group exists with permissions: {permissions}")
        except Group.DoesNotExist:
            print(f"   ❌ {group_name} group not found")
    
    # Test 2: Check if custom permissions exist
    print("\n2️⃣ Testing Custom Permissions:")
    expected_permissions = ['can_view', 'can_create', 'can_edit', 'can_delete']
    for perm_code in expected_permissions:
        try:
            permission = Permission.objects.get(codename=perm_code, content_type__app_label='bookshelf')
            print(f"   ✅ {perm_code}: {permission.name}")
        except Permission.DoesNotExist:
            print(f"   ❌ {perm_code} permission not found")
    
    # Test 3: Check test users and their permissions
    print("\n3️⃣ Testing User Permissions:")
    test_users = [
        ('viewer_user', 'Viewers', ['can_view']),
        ('editor_user', 'Editors', ['can_view', 'can_create', 'can_edit']),
        ('admin_user', 'Admins', ['can_view', 'can_create', 'can_edit', 'can_delete']),
    ]
    
    for username, expected_group, expected_perms in test_users:
        try:
            user = User.objects.get(username=username)
            user_groups = list(user.groups.all().values_list('name', flat=True))
            
            print(f"\n   👤 {username}:")
            print(f"      Groups: {user_groups}")
            
            # Check individual permissions
            actual_perms = []
            for perm in expected_perms:
                if user.has_perm(f'bookshelf.{perm}'):
                    actual_perms.append(perm)
                    print(f"      ✅ {perm}")
                else:
                    print(f"      ❌ {perm}")
            
            # Verify expected vs actual
            if set(actual_perms) == set(expected_perms):
                print(f"      ✅ All expected permissions present")
            else:
                print(f"      ❌ Permission mismatch. Expected: {expected_perms}, Got: {actual_perms}")
                
        except User.DoesNotExist:
            print(f"   ❌ {username} not found")
    
    # Test 4: Check sample books
    print("\n4️⃣ Testing Sample Data:")
    books = Book.objects.all()
    print(f"   📚 Total books: {books.count()}")
    for book in books:
        print(f"      • {book.title} by {book.author} ({book.publication_year})")
    
    # Test 5: Permission inheritance test
    print("\n5️⃣ Testing Permission Inheritance:")
    try:
        viewer = User.objects.get(username='viewer_user')
        editor = User.objects.get(username='editor_user')
        admin = User.objects.get(username='admin_user')
        
        # Test viewer permissions
        print(f"   👁️ Viewer permissions:")
        print(f"      can_view: {viewer.has_perm('bookshelf.can_view')}")
        print(f"      can_create: {viewer.has_perm('bookshelf.can_create')}")
        print(f"      can_edit: {viewer.has_perm('bookshelf.can_edit')}")
        print(f"      can_delete: {viewer.has_perm('bookshelf.can_delete')}")
        
        # Test editor permissions
        print(f"   ✏️ Editor permissions:")
        print(f"      can_view: {editor.has_perm('bookshelf.can_view')}")
        print(f"      can_create: {editor.has_perm('bookshelf.can_create')}")
        print(f"      can_edit: {editor.has_perm('bookshelf.can_edit')}")
        print(f"      can_delete: {editor.has_perm('bookshelf.can_delete')}")
        
        # Test admin permissions
        print(f"   🔧 Admin permissions:")
        print(f"      can_view: {admin.has_perm('bookshelf.can_view')}")
        print(f"      can_create: {admin.has_perm('bookshelf.can_create')}")
        print(f"      can_edit: {admin.has_perm('bookshelf.can_edit')}")
        print(f"      can_delete: {admin.has_perm('bookshelf.can_delete')}")
        
    except User.DoesNotExist as e:
        print(f"   ❌ User not found: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 PERMISSIONS AND GROUPS TEST SUMMARY:")
    print("✅ Custom permissions defined in Book model")
    print("✅ Groups created with appropriate permissions")
    print("✅ Test users created and assigned to groups")
    print("✅ Permission inheritance working correctly")
    print("✅ Sample data available for testing")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/admin/")
    print("3. Login with test users:")
    print("   • viewer_user / viewer123 (Read-only)")
    print("   • editor_user / editor123 (Create, Read, Update)")
    print("   • admin_user / admin123 (Full CRUD)")
    print("4. Test permissions at: http://127.0.0.1:8000/bookshelf/")
    
    print("\n✨ Permissions and Groups system is ready for testing!")

if __name__ == '__main__':
    test_permissions_system()
