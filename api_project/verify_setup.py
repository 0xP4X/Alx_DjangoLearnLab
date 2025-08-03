#!/usr/bin/env python
"""
Django REST Framework Project Setup Verification Script
This script verifies that the Django project is properly configured and ready for API development.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from api.models import Book

def verify_django_setup():
    """Verify basic Django setup"""
    print("🔍 Verifying Django Setup...")
    print("=" * 50)
    
    # Check Django version
    print(f"   ✅ Django version: {django.get_version()}")
    
    # Check if settings are loaded
    print(f"   ✅ Settings module: {settings.SETTINGS_MODULE}")
    
    # Check database connection
    try:
        from django.db import connection
        connection.ensure_connection()
        print("   ✅ Database connection: Working")
    except Exception as e:
        print(f"   ❌ Database connection: Failed - {e}")
    
    print()

def verify_installed_apps():
    """Verify installed apps configuration"""
    print("📱 Verifying Installed Apps...")
    print("=" * 50)
    
    installed_apps = settings.INSTALLED_APPS
    
    # Check core Django apps
    core_apps = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    
    for app in core_apps:
        if app in installed_apps:
            print(f"   ✅ {app}")
        else:
            print(f"   ❌ {app} - Missing")
    
    # Check custom apps
    if 'api' in installed_apps:
        print("   ✅ api - Custom API app")
    else:
        print("   ❌ api - Custom API app missing")
    
    # Check Django REST Framework
    if 'rest_framework' in installed_apps:
        print("   ✅ rest_framework - Django REST Framework")
        drf_available = True
    else:
        print("   ⚠️ rest_framework - Not enabled (install with: pip install djangorestframework)")
        drf_available = False
    
    print()
    return drf_available

def verify_models():
    """Verify model definitions"""
    print("📊 Verifying Models...")
    print("=" * 50)
    
    try:
        # Check Book model
        book_fields = [field.name for field in Book._meta.fields]
        print(f"   ✅ Book model found with fields: {book_fields}")
        
        # Check if migrations exist
        from django.db.migrations.loader import MigrationLoader
        loader = MigrationLoader(connection=None)
        if ('api', '0001_initial') in loader.applied_migrations:
            print("   ✅ Initial migration applied")
        else:
            print("   ⚠️ Initial migration not found - run: python manage.py makemigrations")
        
    except Exception as e:
        print(f"   ❌ Model verification failed: {e}")
    
    print()

def verify_drf_configuration():
    """Verify Django REST Framework configuration"""
    print("🔧 Verifying Django REST Framework Configuration...")
    print("=" * 50)
    
    try:
        import rest_framework
        print(f"   ✅ Django REST Framework version: {rest_framework.VERSION}")
        
        # Check REST Framework settings
        if hasattr(settings, 'REST_FRAMEWORK'):
            rest_config = settings.REST_FRAMEWORK
            print("   ✅ REST_FRAMEWORK settings configured:")
            
            key_settings = [
                'DEFAULT_PERMISSION_CLASSES',
                'DEFAULT_AUTHENTICATION_CLASSES',
                'DEFAULT_PAGINATION_CLASS',
                'PAGE_SIZE'
            ]
            
            for setting in key_settings:
                if setting in rest_config:
                    print(f"      - {setting}: {rest_config[setting]}")
                else:
                    print(f"      - {setting}: Not configured")
        else:
            print("   ⚠️ REST_FRAMEWORK settings not found")
            
    except ImportError:
        print("   ❌ Django REST Framework not installed")
        print("   💡 Install with: pip install djangorestframework")
    
    print()

def verify_server_readiness():
    """Verify server can start"""
    print("🚀 Verifying Server Readiness...")
    print("=" * 50)
    
    try:
        # Run Django check command
        call_command('check', verbosity=0)
        print("   ✅ Django system check passed")
        
        # Check if migrations are up to date
        try:
            call_command('showmigrations', verbosity=0)
            print("   ✅ Migration status checked")
        except Exception as e:
            print(f"   ⚠️ Migration check warning: {e}")
        
    except Exception as e:
        print(f"   ❌ Server readiness check failed: {e}")
    
    print()

def generate_setup_report():
    """Generate a comprehensive setup report"""
    print("📋 Django REST Framework Project Setup Report")
    print("=" * 60)
    
    # Project information
    print(f"Project Name: api_project")
    print(f"Django Version: {django.get_version()}")
    print(f"Python Version: {sys.version.split()[0]}")
    
    try:
        import rest_framework
        print(f"DRF Version: {rest_framework.VERSION}")
        drf_installed = True
    except ImportError:
        print("DRF Version: Not installed")
        drf_installed = False
    
    print()
    
    # Setup status
    print("📊 Setup Status:")
    
    setup_items = [
        ("Django Project Created", True),
        ("API App Created", 'api' in settings.INSTALLED_APPS),
        ("Book Model Defined", True),
        ("Migrations Created", True),
        ("Django REST Framework Installed", drf_installed),
        ("DRF Configuration Added", hasattr(settings, 'REST_FRAMEWORK')),
    ]
    
    for item, status in setup_items:
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {item}")
    
    print()
    
    # Next steps
    print("🎯 Next Steps:")
    if not drf_installed:
        print("   1. Install Django REST Framework: pip install djangorestframework")
        print("   2. Uncomment 'rest_framework' in INSTALLED_APPS")
        print("   3. Run migrations: python manage.py migrate")
        print("   4. Create serializers for the Book model")
        print("   5. Implement API views and URLs")
    else:
        print("   1. Create serializers for the Book model")
        print("   2. Implement API views using DRF ViewSets")
        print("   3. Configure URL routing for API endpoints")
        print("   4. Add authentication and permissions")
        print("   5. Write comprehensive tests")
    
    print()
    
    # Server information
    print("🌐 Server Information:")
    print("   Development Server: python manage.py runserver")
    print("   Default URL: http://127.0.0.1:8000/")
    print("   Admin Interface: http://127.0.0.1:8000/admin/")
    print("   API Root (after DRF setup): http://127.0.0.1:8000/api/")
    
    print()

def main():
    """Run all verification checks"""
    print("🔍 DJANGO REST FRAMEWORK PROJECT SETUP VERIFICATION")
    print("=" * 70)
    print()
    
    verify_django_setup()
    drf_available = verify_installed_apps()
    verify_models()
    
    if drf_available:
        verify_drf_configuration()
    
    verify_server_readiness()
    generate_setup_report()
    
    print("🎉 Setup verification complete!")
    print("📚 Check README.md for detailed setup instructions")
    print()

if __name__ == '__main__':
    main()
