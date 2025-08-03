#!/usr/bin/env python
"""
API Endpoint Testing Script
Tests the Django REST Framework API endpoint for retrieving book information.
"""
import requests
import json
import sys

def test_api_endpoint():
    """Test the books API endpoint"""
    print("🔍 Testing Django REST Framework API Endpoint")
    print("=" * 60)
    
    # API endpoint URL
    base_url = "http://127.0.0.1:8001"
    api_url = f"{base_url}/api/books/"
    
    try:
        print(f"📡 Testing endpoint: {api_url}")
        
        # Make GET request to the API
        response = requests.get(api_url, timeout=10)
        
        # Check response status
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API endpoint is working!")
            
            # Parse JSON response
            data = response.json()
            
            # Display response information
            print(f"📚 Total books: {data.get('count', 'Unknown')}")
            
            # Display first few books
            results = data.get('results', [])
            if results:
                print("\n📖 Sample books:")
                for i, book in enumerate(results[:5]):  # Show first 5 books
                    print(f"   {i+1}. {book.get('title', 'Unknown')} by {book.get('author', 'Unknown')}")
                
                if len(results) > 5:
                    print(f"   ... and {len(results) - 5} more books")
            
            # Display message if present
            message = data.get('message')
            if message:
                print(f"\n💡 Message: {message}")
            
            print("\n🎯 API Response Structure:")
            print(f"   - count: {type(data.get('count')).__name__}")
            print(f"   - results: {type(data.get('results')).__name__} with {len(results)} items")
            if message:
                print(f"   - message: {type(message).__name__}")
            
        else:
            print(f"❌ API endpoint returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the API server")
        print("💡 Make sure the Django development server is running:")
        print("   python manage.py runserver 8001")
        
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: API request timed out")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        
    except json.JSONDecodeError:
        print("❌ JSON Decode Error: Response is not valid JSON")
        print(f"Response content: {response.text}")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

def test_other_endpoints():
    """Test other available endpoints"""
    print("\n🌐 Testing Other Endpoints")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8001"
    endpoints = [
        ("Project Home", "/"),
        ("API Home", "/api/"),
        ("Admin Interface", "/admin/"),
    ]
    
    for name, path in endpoints:
        url = f"{base_url}{path}"
        try:
            response = requests.get(url, timeout=5)
            status_icon = "✅" if response.status_code == 200 else "⚠️"
            print(f"   {status_icon} {name}: {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ {name}: {url} (Error: {str(e)[:50]}...)")

def display_curl_examples():
    """Display curl command examples for testing"""
    print("\n🔧 Testing with curl Commands")
    print("=" * 60)
    
    print("Test the books API endpoint:")
    print("   curl http://127.0.0.1:8001/api/books/")
    
    print("\nTest with pretty JSON formatting:")
    print("   curl -s http://127.0.0.1:8001/api/books/ | python -m json.tool")
    
    print("\nTest with headers:")
    print("   curl -H 'Accept: application/json' http://127.0.0.1:8001/api/books/")

def display_next_steps():
    """Display next steps for DRF integration"""
    print("\n🚀 Next Steps for Full DRF Integration")
    print("=" * 60)
    
    print("1. Install Django REST Framework:")
    print("   pip install djangorestframework")
    
    print("\n2. Enable DRF in settings.py:")
    print("   Uncomment 'rest_framework' in INSTALLED_APPS")
    
    print("\n3. Activate DRF views in api/views.py:")
    print("   Uncomment the DRF imports and BookList class")
    
    print("\n4. Update URL patterns in api/urls.py:")
    print("   Uncomment the DRF URL pattern")
    
    print("\n5. Restart the Django server:")
    print("   python manage.py runserver 8001")
    
    print("\n6. Test the enhanced API:")
    print("   Visit http://127.0.0.1:8001/api/books/ for browsable API")

def main():
    """Main testing function"""
    print("🔍 DJANGO REST FRAMEWORK API ENDPOINT TESTING")
    print("=" * 70)
    
    # Test main API endpoint
    test_api_endpoint()
    
    # Test other endpoints
    test_other_endpoints()
    
    # Display curl examples
    display_curl_examples()
    
    # Display next steps
    display_next_steps()
    
    print("\n🎉 API Endpoint Testing Complete!")
    print("=" * 70)

if __name__ == '__main__':
    # Check if requests library is available
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library not found")
        print("💡 Install with: pip install requests")
        sys.exit(1)
    
    main()
