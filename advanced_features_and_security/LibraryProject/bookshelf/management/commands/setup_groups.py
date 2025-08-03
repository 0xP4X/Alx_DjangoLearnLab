"""
Django management command to set up user groups and assign permissions.
This command creates groups like Editors, Viewers, and Admins and assigns
appropriate permissions to each group.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create user groups and assign permissions for the bookshelf application'

    def handle(self, *args, **options):
        """
        Set up user groups in Django and assign the newly created permissions to these groups.
        Creates groups like Editors, Viewers, and Admins with appropriate permissions.
        """
        
        # Get the content type for the Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create the custom permissions
        can_view, created = Permission.objects.get_or_create(
            codename='can_view',
            name='Can view book',
            content_type=book_content_type,
        )
        
        can_create, created = Permission.objects.get_or_create(
            codename='can_create',
            name='Can create book',
            content_type=book_content_type,
        )
        
        can_edit, created = Permission.objects.get_or_create(
            codename='can_edit',
            name='Can edit book',
            content_type=book_content_type,
        )
        
        can_delete, created = Permission.objects.get_or_create(
            codename='can_delete',
            name='Can delete book',
            content_type=book_content_type,
        )
        
        # Create groups and assign permissions
        
        # 1. Viewers Group - Can only view books
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.clear()
        viewers_group.permissions.add(can_view)
        self.stdout.write(
            self.style.SUCCESS(f'✅ Viewers group created/updated with permissions: can_view')
        )
        
        # 2. Editors Group - Can view, create, and edit books (but not delete)
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.clear()
        editors_group.permissions.add(can_view, can_create, can_edit)
        self.stdout.write(
            self.style.SUCCESS(f'✅ Editors group created/updated with permissions: can_view, can_create, can_edit')
        )
        
        # 3. Admins Group - Full permissions (view, create, edit, delete)
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.clear()
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        self.stdout.write(
            self.style.SUCCESS(f'✅ Admins group created/updated with permissions: can_view, can_create, can_edit, can_delete')
        )
        
        # Display summary
        self.stdout.write(
            self.style.SUCCESS('\n🎯 Groups and Permissions Setup Complete!')
        )
        self.stdout.write('📋 Summary:')
        self.stdout.write(f'   • Viewers: Read-only access to books')
        self.stdout.write(f'   • Editors: Can view, create, and edit books')
        self.stdout.write(f'   • Admins: Full access to all book operations')
        self.stdout.write('\n💡 Use Django admin to assign users to these groups.')
        
        # Display permission details
        self.stdout.write('\n🔐 Available Permissions:')
        for perm in [can_view, can_create, can_edit, can_delete]:
            self.stdout.write(f'   • {perm.codename}: {perm.name}')
