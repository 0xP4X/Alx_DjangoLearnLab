from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Book, CustomUser

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters for these fields in the admin sidebar
    list_filter = ('author', 'publication_year')

    # Enable search functionality for these fields
    search_fields = ('title', 'author')

    # Add ordering
    ordering = ('title',)

    # Number of items per page
    list_per_page = 20

    # Add date hierarchy (if you had date fields)
    # date_hierarchy = 'publication_date'

    # Fields to display in the edit form
    fields = ('title', 'author', 'publication_year')

    # Make certain fields read-only (example)
    # readonly_fields = ('publication_year',)

# Register the Book model with the custom BookAdmin configuration
admin.site.register(Book, BookAdmin)


class CustomUserAdmin(UserAdmin):
    """
    Custom ModelAdmin class that includes configurations for the additional fields
    in the custom user model, ensuring administrators can manage users effectively
    through the Django admin interface.
    """

    # Fields to display in the user list view
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'date_of_birth', 'is_staff', 'is_active', 'date_joined'
    )

    # Fields that can be used for filtering in the admin
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'date_joined',
        'date_of_birth'
    )

    # Fields that can be searched
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Ordering of users in the list view
    ordering = ('username',)

    # Fields to display when editing a user
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('Personal info'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo'),
        }),
    )

    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')

    # Custom methods for the admin
    def get_full_name(self, obj):
        """Display the user's full name in the admin"""
        return obj.get_full_name()
    get_full_name.short_description = _('Full Name')

    def age(self, obj):
        """Display the user's age in the admin"""
        return obj.age
    age.short_description = _('Age')

    # Add custom fields to the list display
    list_display = list_display + ('get_full_name', 'age')


# Register the custom user model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
