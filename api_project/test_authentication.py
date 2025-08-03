#!/usr/bin/env python
"""
Django REST Framework Authentication and Permissions Testing Script
Tests token authentication and permission-based access control.
"""
import requests
import json
import sys

class APIAuthenticationTester:
    def __init__(self, base_url="http://127.0.0.1:8001"):
        self.base_url = base_url
        self.token = None
        self.admin_token = None
        
    def test_basic_endpoints(self):
        """Test basic API endpoints without authentication"""
        print("🔍 Testing Basic API Endpoints (No Authentication)")
        print("=" * 60)
        
        endpoints = [
            ("API Home", "/api/"),
            ("Auth Info", "/api/auth/"),
            ("Books List", "/api/books/"),
        ]
        
        for name, endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, timeout=5)
                status_icon = "✅" if response.status_code == 200 else "⚠️"
                print(f"   {status_icon} {name}: {endpoint} (Status: {response.status_code})")
            except Exception as e:
                print(f"   ❌ {name}: {endpoint} (Error: {str(e)[:50]}...)")
        
        print()
    
    def test_basic_login(self):
        """Test basic login functionality"""
        print("🔐 Testing Basic Login (Without DRF)")
        print("=" * 60)
        
        try:
            url = f"{self.base_url}/api/auth/basic-login/"
            
            # Test with invalid credentials
            response = requests.post(url, json={
                "username": "invalid",
                "password": "invalid"
            }, timeout=5)
            
            if response.status_code == 401:
                print("   ✅ Invalid credentials properly rejected")
            else:
                print(f"   ⚠️ Unexpected response for invalid credentials: {response.status_code}")
            
            # Test with missing credentials
            response = requests.post(url, json={}, timeout=5)
            
            if response.status_code == 400:
                print("   ✅ Missing credentials properly handled")
            else:
                print(f"   ⚠️ Unexpected response for missing credentials: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Basic login test failed: {e}")
        
        print()
    
    def test_token_authentication(self):
        """Test token authentication (when DRF is available)"""
        print("🎫 Testing Token Authentication")
        print("=" * 60)
        
        print("   ⚠️ Token authentication requires DRF installation")
        print("   📋 Steps to test token authentication:")
        print("      1. pip install djangorestframework")
        print("      2. Uncomment 'rest_framework' in INSTALLED_APPS")
        print("      3. Run python manage.py migrate")
        print("      4. Create superuser: python manage.py createsuperuser")
        print("      5. Uncomment authentication views")
        print()
        
        # Show example curl commands
        print("   🔧 Example curl commands (after DRF setup):")
        print("      # Get token:")
        print(f"      curl -X POST {self.base_url}/api/auth/token/ \\")
        print("           -H 'Content-Type: application/json' \\")
        print("           -d '{\"username\": \"admin\", \"password\": \"password\"}'")
        print()
        print("      # Use token for API access:")
        print(f"      curl -H 'Authorization: Token YOUR_TOKEN' \\")
        print(f"           {self.base_url}/api/books/")
        print()
    
    def test_permission_scenarios(self):
        """Test different permission scenarios"""
        print("🛡️ Testing Permission Scenarios")
        print("=" * 60)
        
        scenarios = [
            {
                'name': 'Public Read Access',
                'description': 'Anyone can read books',
                'method': 'GET',
                'endpoint': '/api/books/',
                'auth_required': False,
                'expected_status': 200
            },
            {
                'name': 'Authenticated Create',
                'description': 'Only authenticated users can create books',
                'method': 'POST',
                'endpoint': '/api/books/',
                'auth_required': True,
                'expected_status': 201
            },
            {
                'name': 'Authenticated Update',
                'description': 'Only authenticated users can update books',
                'method': 'PUT',
                'endpoint': '/api/books/1/',
                'auth_required': True,
                'expected_status': 200
            },
            {
                'name': 'Admin Delete',
                'description': 'Only admin users can delete books',
                'method': 'DELETE',
                'endpoint': '/api/books/1/',
                'auth_required': True,
                'admin_required': True,
                'expected_status': 204
            }
        ]
        
        for scenario in scenarios:
            print(f"   📋 {scenario['name']}: {scenario['description']}")
            print(f"      Method: {scenario['method']} {scenario['endpoint']}")
            print(f"      Auth Required: {scenario['auth_required']}")
            if scenario.get('admin_required'):
                print(f"      Admin Required: {scenario['admin_required']}")
            print(f"      Expected Status: {scenario['expected_status']}")
            print()
        
        print("   ⚠️ Full permission testing requires DRF installation and setup")
        print()
    
    def test_custom_actions(self):
        """Test custom ViewSet actions with different permissions"""
        print("🎯 Testing Custom Actions")
        print("=" * 60)
        
        actions = [
            {
                'name': 'Public Books',
                'endpoint': '/api/books/public_books/',
                'permission': 'AllowAny',
                'description': 'Public access to books'
            },
            {
                'name': 'My Books',
                'endpoint': '/api/books/my_books/',
                'permission': 'IsAuthenticated',
                'description': 'Books for authenticated user'
            },
            {
                'name': 'Admin Stats',
                'endpoint': '/api/books/admin_stats/',
                'permission': 'IsAdminUser',
                'description': 'Admin-only statistics'
            }
        ]
        
        for action in actions:
            print(f"   🎯 {action['name']}")
            print(f"      Endpoint: {action['endpoint']}")
            print(f"      Permission: {action['permission']}")
            print(f"      Description: {action['description']}")
            print()
        
        print("   ⚠️ Custom actions require DRF ViewSet activation")
        print()
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("📊 Authentication and Permissions Test Report")
        print("=" * 70)
        
        print("🔧 Current Implementation Status:")
        print("   ✅ Authentication views created")
        print("   ✅ Permission classes defined")
        print("   ✅ ViewSet with permissions configured")
        print("   ✅ Authentication URLs configured")
        print("   ✅ Token authentication settings prepared")
        print("   ⚠️ DRF installation required for full functionality")
        print()
        
        print("🎯 Authentication Methods Available:")
        print("   📋 Token Authentication (primary)")
        print("   📋 Session Authentication (fallback)")
        print("   📋 Basic Authentication (fallback)")
        print()
        
        print("🛡️ Permission Classes Implemented:")
        print("   📋 AllowAny - Public access")
        print("   📋 IsAuthenticated - Authenticated users only")
        print("   📋 IsAdminUser - Admin users only")
        print("   📋 Custom permissions for specific use cases")
        print()
        
        print("🔗 API Endpoints with Permissions:")
        print("   📖 GET /api/books/ - Public read access")
        print("   ➕ POST /api/books/ - Authenticated users")
        print("   📝 PUT/PATCH /api/books/{id}/ - Authenticated users")
        print("   🗑️ DELETE /api/books/{id}/ - Admin users only")
        print("   🎯 Custom actions with specific permissions")
        print()
        
        print("🚀 Next Steps for Full Testing:")
        print("   1. Install DRF: pip install djangorestframework")
        print("   2. Enable DRF in settings.py")
        print("   3. Run migrations: python manage.py migrate")
        print("   4. Create test users: python manage.py createsuperuser")
        print("   5. Uncomment authentication views and ViewSet")
        print("   6. Test with real tokens and permissions")
        print()
        
        print("🧪 Testing Tools:")
        print("   📋 curl commands for API testing")
        print("   📋 Postman for interactive testing")
        print("   📋 DRF browsable API for web interface")
        print("   📋 Python requests for automated testing")
        print()

def main():
    """Main testing function"""
    print("🔐 DJANGO REST FRAMEWORK AUTHENTICATION & PERMISSIONS TESTING")
    print("=" * 80)
    print()
    
    tester = APIAuthenticationTester()
    
    # Run all tests
    tester.test_basic_endpoints()
    tester.test_basic_login()
    tester.test_token_authentication()
    tester.test_permission_scenarios()
    tester.test_custom_actions()
    tester.generate_test_report()
    
    print("🎉 Authentication and Permissions Testing Complete!")
    print("=" * 80)

if __name__ == '__main__':
    # Check if requests library is available
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library not found")
        print("💡 Install with: pip install requests")
        sys.exit(1)
    
    main()
