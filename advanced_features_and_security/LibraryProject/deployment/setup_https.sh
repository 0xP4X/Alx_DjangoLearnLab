#!/bin/bash

# HTTPS Setup Script for Django Application
# This script helps set up HTTPS with Let's Encrypt SSL certificates
# and configures the web server for secure connections

set -e  # Exit on any error

# Configuration variables
DOMAIN="yourdomain.com"
EMAIL="admin@yourdomain.com"
WEBSERVER="nginx"  # Options: nginx, apache
DJANGO_PROJECT_PATH="/path/to/your/django/project"
STATIC_ROOT="/path/to/your/django/static"
MEDIA_ROOT="/path/to/your/django/media"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root (use sudo)"
    fi
}

# Update system packages
update_system() {
    log "Updating system packages..."
    apt-get update -y
    apt-get upgrade -y
}

# Install required packages
install_dependencies() {
    log "Installing required packages..."
    
    # Install common dependencies
    apt-get install -y curl wget software-properties-common
    
    # Install web server
    if [[ "$WEBSERVER" == "nginx" ]]; then
        apt-get install -y nginx
    elif [[ "$WEBSERVER" == "apache" ]]; then
        apt-get install -y apache2
        a2enmod ssl
        a2enmod headers
        a2enmod proxy
        a2enmod proxy_http
        a2enmod rewrite
    fi
    
    # Install Certbot for Let's Encrypt
    apt-get install -y certbot
    
    if [[ "$WEBSERVER" == "nginx" ]]; then
        apt-get install -y python3-certbot-nginx
    elif [[ "$WEBSERVER" == "apache" ]]; then
        apt-get install -y python3-certbot-apache
    fi
}

# Configure firewall
configure_firewall() {
    log "Configuring firewall..."
    
    # Install UFW if not present
    apt-get install -y ufw
    
    # Configure firewall rules
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
    
    log "Firewall configured successfully"
}

# Obtain SSL certificate
obtain_ssl_certificate() {
    log "Obtaining SSL certificate from Let's Encrypt..."
    
    # Stop web server temporarily
    systemctl stop $WEBSERVER
    
    # Obtain certificate
    certbot certonly --standalone \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        --domains $DOMAIN \
        --non-interactive
    
    if [[ $? -eq 0 ]]; then
        log "SSL certificate obtained successfully"
    else
        error "Failed to obtain SSL certificate"
    fi
}

# Configure web server
configure_webserver() {
    log "Configuring $WEBSERVER for HTTPS..."
    
    if [[ "$WEBSERVER" == "nginx" ]]; then
        # Copy Nginx configuration
        cp nginx_https.conf /etc/nginx/sites-available/django-https
        
        # Update configuration with actual paths
        sed -i "s|yourdomain.com|$DOMAIN|g" /etc/nginx/sites-available/django-https
        sed -i "s|/path/to/your/certificate.crt|/etc/letsencrypt/live/$DOMAIN/fullchain.pem|g" /etc/nginx/sites-available/django-https
        sed -i "s|/path/to/your/private.key|/etc/letsencrypt/live/$DOMAIN/privkey.pem|g" /etc/nginx/sites-available/django-https
        sed -i "s|/path/to/your/ca-bundle.crt|/etc/letsencrypt/live/$DOMAIN/chain.pem|g" /etc/nginx/sites-available/django-https
        sed -i "s|/path/to/your/django/static/|$STATIC_ROOT/|g" /etc/nginx/sites-available/django-https
        sed -i "s|/path/to/your/django/media/|$MEDIA_ROOT/|g" /etc/nginx/sites-available/django-https
        
        # Enable site
        ln -sf /etc/nginx/sites-available/django-https /etc/nginx/sites-enabled/
        rm -f /etc/nginx/sites-enabled/default
        
        # Test configuration
        nginx -t
        
    elif [[ "$WEBSERVER" == "apache" ]]; then
        # Copy Apache configuration
        cp apache_https.conf /etc/apache2/sites-available/django-https.conf
        
        # Update configuration with actual paths
        sed -i "s|yourdomain.com|$DOMAIN|g" /etc/apache2/sites-available/django-https.conf
        sed -i "s|/path/to/your/certificate.crt|/etc/letsencrypt/live/$DOMAIN/fullchain.pem|g" /etc/apache2/sites-available/django-https.conf
        sed -i "s|/path/to/your/private.key|/etc/letsencrypt/live/$DOMAIN/privkey.pem|g" /etc/apache2/sites-available/django-https.conf
        sed -i "s|/path/to/your/ca-bundle.crt|/etc/letsencrypt/live/$DOMAIN/chain.pem|g" /etc/apache2/sites-available/django-https.conf
        sed -i "s|/path/to/your/django/static/|$STATIC_ROOT/|g" /etc/apache2/sites-available/django-https.conf
        sed -i "s|/path/to/your/django/media/|$MEDIA_ROOT/|g" /etc/apache2/sites-available/django-https.conf
        
        # Enable site and modules
        a2ensite django-https
        a2dissite 000-default
        
        # Test configuration
        apache2ctl configtest
    fi
}

# Configure Django for HTTPS
configure_django() {
    log "Configuring Django for HTTPS..."
    
    # Set environment variable for HTTPS
    echo "export DJANGO_HTTPS_ENABLED=True" >> /etc/environment
    
    # Create systemd environment file for Django service
    mkdir -p /etc/systemd/system/django.service.d/
    cat > /etc/systemd/system/django.service.d/https.conf << EOF
[Service]
Environment="DJANGO_HTTPS_ENABLED=True"
EOF
    
    log "Django HTTPS configuration completed"
}

# Setup certificate auto-renewal
setup_auto_renewal() {
    log "Setting up automatic certificate renewal..."
    
    # Create renewal script
    cat > /usr/local/bin/renew-certificates.sh << 'EOF'
#!/bin/bash
certbot renew --quiet
systemctl reload nginx apache2 2>/dev/null || true
EOF
    
    chmod +x /usr/local/bin/renew-certificates.sh
    
    # Add cron job for automatic renewal
    (crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/renew-certificates.sh") | crontab -
    
    log "Automatic certificate renewal configured"
}

# Start services
start_services() {
    log "Starting services..."
    
    systemctl enable $WEBSERVER
    systemctl start $WEBSERVER
    systemctl reload $WEBSERVER
    
    log "Services started successfully"
}

# Verify HTTPS setup
verify_https() {
    log "Verifying HTTPS setup..."
    
    # Wait a moment for services to start
    sleep 5
    
    # Test HTTPS connection
    if curl -s -I https://$DOMAIN | grep -q "HTTP/"; then
        log "HTTPS is working correctly!"
    else
        warn "HTTPS verification failed. Please check the configuration."
    fi
    
    # Test HTTP to HTTPS redirect
    if curl -s -I http://$DOMAIN | grep -q "301\|302"; then
        log "HTTP to HTTPS redirect is working!"
    else
        warn "HTTP to HTTPS redirect may not be working correctly."
    fi
}

# Main execution
main() {
    log "Starting HTTPS setup for Django application..."
    
    check_root
    update_system
    install_dependencies
    configure_firewall
    obtain_ssl_certificate
    configure_webserver
    configure_django
    setup_auto_renewal
    start_services
    verify_https
    
    log "HTTPS setup completed successfully!"
    log "Your Django application should now be accessible at https://$DOMAIN"
    log "HTTP requests will be automatically redirected to HTTPS"
    
    warn "Don't forget to:"
    warn "1. Update your Django settings.py with the correct domain in ALLOWED_HOSTS"
    warn "2. Restart your Django application to apply HTTPS settings"
    warn "3. Test all functionality to ensure everything works over HTTPS"
}

# Run main function
main "$@"
