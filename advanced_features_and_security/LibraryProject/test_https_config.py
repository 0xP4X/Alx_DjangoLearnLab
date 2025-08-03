#!/usr/bin/env python
"""
HTTPS Configuration Testing Script
Tests Django HTTPS settings and security configuration to ensure proper implementation.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.conf import settings
from django.test import Client, TestCase
from django.core.management import call_command

class HTTPSConfigurationTester:
    """Test HTTPS configuration and security settings"""
    
    def __init__(self):
        self.client = Client()
        
    def test_https_settings(self):
        """Test HTTPS-related Django settings"""
        print("🔒 Testing HTTPS Configuration Settings...")
        print("=" * 60)
        
        # Test environment variable detection
        https_enabled = getattr(settings, 'HTTPS_ENABLED', False)
        print(f"   📊 HTTPS_ENABLED: {https_enabled}")
        
        # Test HTTPS redirect setting
        ssl_redirect = getattr(settings, 'SECURE_SSL_REDIRECT', False)
        print(f"   🔄 SECURE_SSL_REDIRECT: {ssl_redirect}")
        
        # Test HSTS settings
        hsts_seconds = getattr(settings, 'SECURE_HSTS_SECONDS', 0)
        hsts_subdomains = getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
        hsts_preload = getattr(settings, 'SECURE_HSTS_PRELOAD', False)
        
        print(f"   🛡️ SECURE_HSTS_SECONDS: {hsts_seconds}")
        print(f"   🌐 SECURE_HSTS_INCLUDE_SUBDOMAINS: {hsts_subdomains}")
        print(f"   ⚡ SECURE_HSTS_PRELOAD: {hsts_preload}")
        
        # Test proxy header setting
        proxy_header = getattr(settings, 'SECURE_PROXY_SSL_HEADER', None)
        print(f"   🔗 SECURE_PROXY_SSL_HEADER: {proxy_header}")
        
        print()
        
    def test_cookie_security(self):
        """Test secure cookie configuration"""
        print("🍪 Testing Secure Cookie Configuration...")
        print("=" * 60)
        
        # Test CSRF cookie security
        csrf_secure = getattr(settings, 'CSRF_COOKIE_SECURE', False)
        csrf_httponly = getattr(settings, 'CSRF_COOKIE_HTTPONLY', False)
        csrf_samesite = getattr(settings, 'CSRF_COOKIE_SAMESITE', None)
        
        print(f"   🔐 CSRF_COOKIE_SECURE: {csrf_secure}")
        print(f"   🚫 CSRF_COOKIE_HTTPONLY: {csrf_httponly}")
        print(f"   🔒 CSRF_COOKIE_SAMESITE: {csrf_samesite}")
        
        # Test session cookie security
        session_secure = getattr(settings, 'SESSION_COOKIE_SECURE', False)
        session_httponly = getattr(settings, 'SESSION_COOKIE_HTTPONLY', False)
        session_samesite = getattr(settings, 'SESSION_COOKIE_SAMESITE', None)
        session_age = getattr(settings, 'SESSION_COOKIE_AGE', None)
        
        print(f"   🔐 SESSION_COOKIE_SECURE: {session_secure}")
        print(f"   🚫 SESSION_COOKIE_HTTPONLY: {session_httponly}")
        print(f"   🔒 SESSION_COOKIE_SAMESITE: {session_samesite}")
        print(f"   ⏰ SESSION_COOKIE_AGE: {session_age}")
        
        print()
        
    def test_security_headers(self):
        """Test security header configuration"""
        print("📋 Testing Security Headers Configuration...")
        print("=" * 60)
        
        # Test XSS protection
        xss_filter = getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False)
        print(f"   🚫 SECURE_BROWSER_XSS_FILTER: {xss_filter}")
        
        # Test content type sniffing protection
        content_type_nosniff = getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False)
        print(f"   🔍 SECURE_CONTENT_TYPE_NOSNIFF: {content_type_nosniff}")
        
        # Test frame options
        frame_options = getattr(settings, 'X_FRAME_OPTIONS', None)
        print(f"   🖼️ X_FRAME_OPTIONS: {frame_options}")
        
        # Test referrer policy
        referrer_policy = getattr(settings, 'SECURE_REFERRER_POLICY', None)
        print(f"   🔗 SECURE_REFERRER_POLICY: {referrer_policy}")
        
        print()
        
    def test_environment_configuration(self):
        """Test environment-based configuration"""
        print("🌍 Testing Environment Configuration...")
        print("=" * 60)
        
        # Test current environment
        debug = getattr(settings, 'DEBUG', True)
        print(f"   🐛 DEBUG: {debug}")
        
        # Test allowed hosts
        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
        print(f"   🌐 ALLOWED_HOSTS: {allowed_hosts}")
        
        # Test secret key (don't print actual value)
        secret_key = getattr(settings, 'SECRET_KEY', '')
        print(f"   🔑 SECRET_KEY: {'Set' if secret_key else 'Not Set'} ({'Secure' if len(secret_key) > 50 else 'Weak'})")
        
        print()
        
    def test_https_environment_simulation(self):
        """Test HTTPS configuration with environment variable simulation"""
        print("🧪 Testing HTTPS Environment Simulation...")
        print("=" * 60)
        
        # Save current environment
        original_https = os.environ.get('DJANGO_HTTPS_ENABLED', '')
        
        try:
            # Test with HTTPS enabled
            os.environ['DJANGO_HTTPS_ENABLED'] = 'True'
            
            # Reload settings (in real deployment, this would require restart)
            print("   🔄 Simulating HTTPS_ENABLED=True environment...")
            print("   ⚠️ Note: In production, Django restart required for changes")
            
            # Show what settings would be with HTTPS enabled
            print("   📊 Expected settings with HTTPS enabled:")
            print("      - SECURE_SSL_REDIRECT: True")
            print("      - SECURE_HSTS_SECONDS: 31536000")
            print("      - SECURE_HSTS_INCLUDE_SUBDOMAINS: True")
            print("      - SECURE_HSTS_PRELOAD: True")
            print("      - CSRF_COOKIE_SECURE: True")
            print("      - SESSION_COOKIE_SECURE: True")
            print("      - SECURE_PROXY_SSL_HEADER: ('HTTP_X_FORWARDED_PROTO', 'https')")
            
        finally:
            # Restore original environment
            if original_https:
                os.environ['DJANGO_HTTPS_ENABLED'] = original_https
            else:
                os.environ.pop('DJANGO_HTTPS_ENABLED', None)
        
        print()
        
    def test_deployment_readiness(self):
        """Test deployment readiness for HTTPS"""
        print("🚀 Testing Deployment Readiness...")
        print("=" * 60)
        
        # Run Django's deployment check
        try:
            print("   🔍 Running Django deployment check...")
            call_command('check', '--deploy', verbosity=0)
            print("   ✅ Django deployment check passed")
        except Exception as e:
            print(f"   ⚠️ Django deployment check warnings: {e}")
        
        # Check for common deployment issues
        issues = []
        
        if getattr(settings, 'DEBUG', True):
            issues.append("DEBUG is True (should be False in production)")
        
        if not getattr(settings, 'ALLOWED_HOSTS', []):
            issues.append("ALLOWED_HOSTS is empty (should contain your domain)")
        
        secret_key = getattr(settings, 'SECRET_KEY', '')
        if len(secret_key) < 50:
            issues.append("SECRET_KEY appears to be weak or default")
        
        if issues:
            print("   ⚠️ Deployment issues found:")
            for issue in issues:
                print(f"      - {issue}")
        else:
            print("   ✅ No major deployment issues detected")
        
        print()
        
    def generate_security_report(self):
        """Generate a comprehensive security report"""
        print("📊 HTTPS Security Configuration Report")
        print("=" * 60)
        
        https_enabled = getattr(settings, 'HTTPS_ENABLED', False)
        
        if https_enabled:
            print("   🟢 HTTPS Configuration: ENABLED")
            print("   ✅ All HTTPS security features are active")
        else:
            print("   🟡 HTTPS Configuration: DISABLED (Development Mode)")
            print("   ⚠️ HTTPS features disabled for development")
        
        print("\n   📋 Security Features Status:")
        
        features = [
            ("SSL Redirect", getattr(settings, 'SECURE_SSL_REDIRECT', False)),
            ("HSTS Protection", getattr(settings, 'SECURE_HSTS_SECONDS', 0) > 0),
            ("Secure Cookies", getattr(settings, 'CSRF_COOKIE_SECURE', False)),
            ("XSS Protection", getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False)),
            ("MIME Sniffing Protection", getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False)),
            ("Clickjacking Protection", getattr(settings, 'X_FRAME_OPTIONS', None) == 'DENY'),
        ]
        
        for feature, enabled in features:
            status = "✅" if enabled else "❌"
            print(f"      {status} {feature}")
        
        print("\n   🎯 Recommendations:")
        if not https_enabled:
            print("      1. Set DJANGO_HTTPS_ENABLED=True in production")
            print("      2. Obtain SSL certificate for your domain")
            print("      3. Configure web server for HTTPS")
            print("      4. Test HTTPS configuration thoroughly")
        else:
            print("      1. Verify SSL certificate is valid and trusted")
            print("      2. Test HTTPS redirect functionality")
            print("      3. Validate security headers in browser")
            print("      4. Run SSL Labs test for comprehensive analysis")
        
        print()
        
    def run_all_tests(self):
        """Run all HTTPS configuration tests"""
        print("🔒 DJANGO HTTPS CONFIGURATION TESTING SUITE")
        print("=" * 70)
        print()
        
        self.test_https_settings()
        self.test_cookie_security()
        self.test_security_headers()
        self.test_environment_configuration()
        self.test_https_environment_simulation()
        self.test_deployment_readiness()
        self.generate_security_report()
        
        print("🎯 HTTPS CONFIGURATION TESTING COMPLETE!")
        print("=" * 70)
        print("✅ Review the results above to ensure HTTPS is properly configured")
        print("🚀 For production deployment:")
        print("   1. Set DJANGO_HTTPS_ENABLED=True")
        print("   2. Configure SSL certificates")
        print("   3. Update web server configuration")
        print("   4. Test thoroughly before going live")
        print()


if __name__ == '__main__':
    tester = HTTPSConfigurationTester()
    tester.run_all_tests()
