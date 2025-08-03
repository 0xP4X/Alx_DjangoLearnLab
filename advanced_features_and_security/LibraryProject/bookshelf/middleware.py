"""
Security Middleware for Django Application
Implements Content Security Policy (CSP) and other security headers
to protect against XSS, clickjacking, and other client-side attacks.
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('django.security')


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers to all responses.
    Implements Content Security Policy (CSP) and other security measures.
    """
    
    def process_response(self, request, response):
        """
        Add security headers to the response.
        
        Security Headers Implemented:
        - Content Security Policy (CSP)
        - X-Content-Type-Options
        - X-Frame-Options
        - X-XSS-Protection
        - Referrer-Policy
        - Permissions-Policy
        """
        
        # Content Security Policy (CSP) Header
        # Reduces XSS risk by specifying which domains can load content
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",  # Allow inline scripts for development
            "style-src 'self' 'unsafe-inline'",   # Allow inline styles for development
            "img-src 'self' data: https:",
            "font-src 'self' https:",
            "connect-src 'self'",
            "frame-ancestors 'none'",  # Prevent framing
            "base-uri 'self'",
            "form-action 'self'",
            "upgrade-insecure-requests",  # Upgrade HTTP to HTTPS
        ]
        
        # In production, remove 'unsafe-inline' and use nonces or hashes
        if not settings.DEBUG:
            csp_directives = [
                directive.replace(" 'unsafe-inline'", "") 
                for directive in csp_directives
            ]
        
        response['Content-Security-Policy'] = "; ".join(csp_directives)
        
        # Additional Security Headers
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Clickjacking protection (already set by Django's XFrameOptionsMiddleware)
        # response['X-Frame-Options'] = 'DENY'
        
        # XSS Protection (legacy, but still useful for older browsers)
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy - control referrer information
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy - control browser features
        permissions_policy = [
            "geolocation=()",
            "microphone=()",
            "camera=()",
            "payment=()",
            "usb=()",
            "magnetometer=()",
            "gyroscope=()",
            "speaker=()",
        ]
        response['Permissions-Policy'] = ", ".join(permissions_policy)
        
        # Feature Policy (deprecated but still supported by some browsers)
        response['Feature-Policy'] = "; ".join([
            "geolocation 'none'",
            "microphone 'none'",
            "camera 'none'",
            "payment 'none'",
            "usb 'none'",
        ])
        
        # Cache Control for sensitive pages
        if hasattr(request, 'user') and request.user.is_authenticated:
            if request.path.startswith('/admin/') or 'edit' in request.path or 'create' in request.path:
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
        
        return response


class SecurityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log security-related events and suspicious activities.
    """
    
    def process_request(self, request):
        """
        Log security-relevant request information.
        """
        # Log suspicious request patterns
        suspicious_patterns = [
            'script',
            'javascript:',
            '<iframe',
            'eval(',
            'document.cookie',
            'union select',
            'drop table',
            '../',
            '..\\',
        ]
        
        # Check for suspicious content in request
        request_data = str(request.GET) + str(request.POST) + str(request.path)
        
        for pattern in suspicious_patterns:
            if pattern.lower() in request_data.lower():
                logger.warning(
                    f'Suspicious request pattern detected: {pattern} '
                    f'from IP {self.get_client_ip(request)} '
                    f'User: {getattr(request.user, "username", "Anonymous")} '
                    f'Path: {request.path}'
                )
                break
        
        return None
    
    def process_response(self, request, response):
        """
        Log security-relevant response information.
        """
        # Log failed authentication attempts
        if response.status_code == 403:
            logger.warning(
                f'403 Forbidden response for IP {self.get_client_ip(request)} '
                f'User: {getattr(request.user, "username", "Anonymous")} '
                f'Path: {request.path}'
            )
        
        # Log server errors that might indicate attacks
        if response.status_code >= 500:
            logger.error(
                f'Server error {response.status_code} for IP {self.get_client_ip(request)} '
                f'User: {getattr(request.user, "username", "Anonymous")} '
                f'Path: {request.path}'
            )
        
        return response
    
    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        Handles proxy headers securely.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Take the first IP in the chain (most recent proxy)
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RateLimitingMiddleware(MiddlewareMixin):
    """
    Simple rate limiting middleware to prevent abuse.
    In production, use a more sophisticated solution like django-ratelimit.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}  # In production, use Redis or database
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Implement basic rate limiting based on IP address.
        """
        if not settings.DEBUG:  # Only enable in production
            client_ip = self.get_client_ip(request)
            
            # Simple rate limiting: max 100 requests per minute per IP
            import time
            current_time = int(time.time() / 60)  # Current minute
            
            if client_ip not in self.request_counts:
                self.request_counts[client_ip] = {}
            
            if current_time not in self.request_counts[client_ip]:
                self.request_counts[client_ip][current_time] = 0
            
            self.request_counts[client_ip][current_time] += 1
            
            # Clean old entries
            for minute in list(self.request_counts[client_ip].keys()):
                if minute < current_time - 5:  # Keep last 5 minutes
                    del self.request_counts[client_ip][minute]
            
            # Check rate limit
            if self.request_counts[client_ip][current_time] > 100:
                logger.warning(f'Rate limit exceeded for IP {client_ip}')
                from django.http import HttpResponseTooManyRequests
                return HttpResponseTooManyRequests("Rate limit exceeded")
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
