"""
Django management command to create test users and assign them to groups.
This command creates test users for different permission levels and assigns
them to the appropriate groups for testing the permission system.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from bookshelf.models import Book

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users and assign them to different groups for testing permissions'

    def handle(self, *args, **options):
        """
        Create test users and assign them to different groups.
        Testing Approach: Create test users and assign them to different groups.
        """
        
        # Create test users for different permission levels
        
        # 1. Viewer User - Can only view books
        viewer_user, created = User.objects.get_or_create(
            username='viewer_user',
            defaults={
                'email': 'viewer@example.com',
                'first_name': 'View',
                'last_name': 'User',
                'is_active': True,
            }
        )
        if created:
            viewer_user.set_password('viewer123')
            viewer_user.save()
        
        # Assign to Viewers group
        viewers_group = Group.objects.get(name='Viewers')
        viewer_user.groups.clear()
        viewer_user.groups.add(viewers_group)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Viewer user created: {viewer_user.username} (Group: Viewers)')
        )
        
        # 2. Editor User - Can view, create, and edit books
        editor_user, created = User.objects.get_or_create(
            username='editor_user',
            defaults={
                'email': 'editor@example.com',
                'first_name': 'Edit',
                'last_name': 'User',
                'is_active': True,
            }
        )
        if created:
            editor_user.set_password('editor123')
            editor_user.save()
        
        # Assign to Editors group
        editors_group = Group.objects.get(name='Editors')
        editor_user.groups.clear()
        editor_user.groups.add(editors_group)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Editor user created: {editor_user.username} (Group: Editors)')
        )
        
        # 3. Admin User - Full permissions
        admin_user, created = User.objects.get_or_create(
            username='admin_user',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_active': True,
                'is_staff': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        # Assign to Admins group
        admins_group = Group.objects.get(name='Admins')
        admin_user.groups.clear()
        admin_user.groups.add(admins_group)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Admin user created: {admin_user.username} (Group: Admins)')
        )
        
        # Create some sample books for testing
        sample_books = [
            {'title': 'Django for Beginners', 'author': 'William S. Vincent', 'publication_year': 2022},
            {'title': 'Two Scoops of Django', 'author': 'Daniel Roy Greenfeld', 'publication_year': 2021},
            {'title': 'Django REST Framework', 'author': 'Tom Christie', 'publication_year': 2023},
        ]
        
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'📚 Sample book created: {book.title}')
        
        # Display summary
        self.stdout.write(
            self.style.SUCCESS('\n🎯 Test Users and Sample Data Setup Complete!')
        )
        self.stdout.write('👥 Test Users Created:')
        self.stdout.write(f'   • viewer_user / viewer123 (Viewers group) - Read-only access')
        self.stdout.write(f'   • editor_user / editor123 (Editors group) - Create, read, update access')
        self.stdout.write(f'   • admin_user / admin123 (Admins group) - Full CRUD access')
        
        self.stdout.write('\n🧪 Testing Instructions:')
        self.stdout.write('1. Log in as different users at /admin/')
        self.stdout.write('2. Visit /bookshelf/ to test permissions')
        self.stdout.write('3. Try accessing different views with each user')
        self.stdout.write('4. Verify that permissions are enforced correctly')
        
        # Display permission summary
        self.stdout.write('\n🔐 Permission Summary:')
        self.stdout.write('   • Viewers: can_view only')
        self.stdout.write('   • Editors: can_view, can_create, can_edit')
        self.stdout.write('   • Admins: can_view, can_create, can_edit, can_delete')
