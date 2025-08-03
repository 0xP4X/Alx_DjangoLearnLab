#!/usr/bin/env python
"""
Security Testing Script for Django Application
Tests various security measures and configurations to ensure proper protection
against common vulnerabilities.
"""
import os
import sys
import django
import requests
from urllib.parse import urljoin

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from bookshelf.models import Book
from bookshelf.forms import SecureBookForm, SecureSearchForm

User = get_user_model()

class SecurityTester:
    """Comprehensive security testing for the Django application"""
    
    def __init__(self):
        self.client = Client()
        self.base_url = 'http://127.0.0.1:8000'
        
    def test_security_settings(self):
        """Test security-related Django settings"""
        print("🔒 Testing Security Settings...")
        print("=" * 50)
        
        # Test security settings
        security_checks = [
            ('SECURE_BROWSER_XSS_FILTER', getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False)),
            ('SECURE_CONTENT_TYPE_NOSNIFF', getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False)),
            ('X_FRAME_OPTIONS', getattr(settings, 'X_FRAME_OPTIONS', None)),
            ('CSRF_COOKIE_HTTPONLY', getattr(settings, 'CSRF_COOKIE_HTTPONLY', False)),
            ('SESSION_COOKIE_HTTPONLY', getattr(settings, 'SESSION_COOKIE_HTTPONLY', False)),
        ]
        
        for setting_name, value in security_checks:
            status = "✅" if value else "❌"
            print(f"   {status} {setting_name}: {value}")
        
        # Test password hashers
        password_hashers = getattr(settings, 'PASSWORD_HASHERS', [])
        if 'django.contrib.auth.hashers.Argon2PasswordHasher' in password_hashers:
            print("   ✅ Strong password hashing (Argon2) configured")
        else:
            print("   ❌ Weak password hashing configuration")
        
        print()
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        print("🛡️ Testing CSRF Protection...")
        print("=" * 50)
        
        try:
            # Create a test user
            user = User.objects.create_user(username='testuser', password='testpass123')
            self.client.login(username='testuser', password='testpass123')
            
            # Test CSRF protection on book creation
            response = self.client.post('/bookshelf/book/create/', {
                'title': 'Test Book',
                'author': 'Test Author',
                'publication_year': 2023
            })
            
            # Should fail without CSRF token
            if response.status_code == 403:
                print("   ✅ CSRF protection working - form rejected without token")
            else:
                print("   ❌ CSRF protection failed - form accepted without token")
            
            # Test with CSRF token
            response = self.client.get('/bookshelf/book/create/')
            csrf_token = response.context['csrf_token']
            
            response = self.client.post('/bookshelf/book/create/', {
                'title': 'Test Book',
                'author': 'Test Author',
                'publication_year': 2023,
                'csrfmiddlewaretoken': csrf_token
            })
            
            if response.status_code in [200, 302]:
                print("   ✅ CSRF protection working - form accepted with valid token")
            else:
                print("   ❌ CSRF protection issue - form rejected with valid token")
                
        except Exception as e:
            print(f"   ❌ CSRF test error: {e}")
        
        print()
    
    def test_xss_prevention(self):
        """Test XSS prevention in forms and templates"""
        print("🚫 Testing XSS Prevention...")
        print("=" * 50)
        
        xss_payloads = [
            '<script>alert("XSS")</script>',
            'javascript:alert("XSS")',
            '<img src="x" onerror="alert(\'XSS\')">',
            '<iframe src="javascript:alert(\'XSS\')"></iframe>',
            'onmouseover="alert(\'XSS\')"',
        ]
        
        for payload in xss_payloads:
            try:
                form = SecureBookForm(data={
                    'title': payload,
                    'author': 'Test Author',
                    'publication_year': 2023
                })
                
                if form.is_valid():
                    print(f"   ❌ XSS payload accepted: {payload[:30]}...")
                else:
                    print(f"   ✅ XSS payload rejected: {payload[:30]}...")
                    
            except Exception as e:
                print(f"   ✅ XSS payload caused validation error: {payload[:30]}...")
        
        print()
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention in search functionality"""
        print("💉 Testing SQL Injection Prevention...")
        print("=" * 50)
        
        sql_payloads = [
            "'; DROP TABLE books; --",
            "' UNION SELECT * FROM auth_user --",
            "' OR '1'='1",
            "'; INSERT INTO books VALUES (999, 'Hacked', 'Hacker', 2023); --",
            "' AND (SELECT COUNT(*) FROM auth_user) > 0 --",
        ]
        
        for payload in sql_payloads:
            try:
                form = SecureSearchForm(data={
                    'query': payload,
                    'search_type': 'title'
                })
                
                if form.is_valid():
                    print(f"   ❌ SQL injection payload accepted: {payload[:30]}...")
                else:
                    print(f"   ✅ SQL injection payload rejected: {payload[:30]}...")
                    
            except Exception as e:
                print(f"   ✅ SQL injection payload caused error: {payload[:30]}...")
        
        print()
    
    def test_security_headers(self):
        """Test security headers in HTTP responses"""
        print("📋 Testing Security Headers...")
        print("=" * 50)
        
        try:
            # Make a request to test security headers
            response = self.client.get('/bookshelf/')
            
            expected_headers = [
                ('Content-Security-Policy', 'CSP header'),
                ('X-Content-Type-Options', 'MIME sniffing protection'),
                ('X-XSS-Protection', 'XSS protection'),
                ('X-Frame-Options', 'Clickjacking protection'),
                ('Referrer-Policy', 'Referrer policy'),
            ]
            
            for header, description in expected_headers:
                if header in response:
                    print(f"   ✅ {description}: {response[header][:50]}...")
                else:
                    print(f"   ❌ Missing {description}")
                    
        except Exception as e:
            print(f"   ❌ Security headers test error: {e}")
        
        print()
    
    def test_permission_enforcement(self):
        """Test permission-based access control"""
        print("🔐 Testing Permission Enforcement...")
        print("=" * 50)
        
        try:
            # Test unauthenticated access
            self.client.logout()
            response = self.client.get('/bookshelf/')
            
            if response.status_code in [302, 403]:
                print("   ✅ Unauthenticated access properly restricted")
            else:
                print("   ❌ Unauthenticated access allowed")
            
            # Test with user without permissions
            user = User.objects.create_user(username='noperm', password='testpass123')
            self.client.login(username='noperm', password='testpass123')
            
            response = self.client.get('/bookshelf/book/create/')
            if response.status_code == 403:
                print("   ✅ Permission enforcement working - create access denied")
            else:
                print("   ❌ Permission enforcement failed - create access allowed")
                
        except Exception as e:
            print(f"   ❌ Permission test error: {e}")
        
        print()
    
    def test_input_validation(self):
        """Test comprehensive input validation"""
        print("✅ Testing Input Validation...")
        print("=" * 50)
        
        # Test invalid input patterns
        invalid_inputs = [
            {'title': '', 'author': 'Test', 'publication_year': 2023},  # Empty title
            {'title': 'A', 'author': 'Test', 'publication_year': 2023},  # Too short
            {'title': 'A' * 201, 'author': 'Test', 'publication_year': 2023},  # Too long
            {'title': 'Test', 'author': '', 'publication_year': 2023},  # Empty author
            {'title': 'Test', 'author': 'Test123', 'publication_year': 2023},  # Invalid author
            {'title': 'Test', 'author': 'Test', 'publication_year': 999},  # Invalid year
            {'title': 'Test', 'author': 'Test', 'publication_year': 2031},  # Future year
        ]
        
        for i, data in enumerate(invalid_inputs):
            form = SecureBookForm(data=data)
            if form.is_valid():
                print(f"   ❌ Invalid input {i+1} accepted: {data}")
            else:
                print(f"   ✅ Invalid input {i+1} rejected: {list(form.errors.keys())}")
        
        print()
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🔒 DJANGO SECURITY TESTING SUITE")
        print("=" * 60)
        print()
        
        self.test_security_settings()
        self.test_csrf_protection()
        self.test_xss_prevention()
        self.test_sql_injection_prevention()
        self.test_security_headers()
        self.test_permission_enforcement()
        self.test_input_validation()
        
        print("🎯 SECURITY TESTING COMPLETE!")
        print("=" * 60)
        print("✅ Review the results above to ensure all security measures are working")
        print("🚀 For production deployment, ensure all settings are properly configured")
        print()


if __name__ == '__main__':
    tester = SecurityTester()
    tester.run_all_tests()
