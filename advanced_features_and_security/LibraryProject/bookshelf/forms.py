"""
Secure Django Forms Implementation
This module demonstrates secure form handling with proper validation,
sanitization, and protection against common vulnerabilities.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.core.validators import RegexValidator, MinLengthValidator
import re
from .models import Book


class SecureBookForm(forms.ModelForm):
    """
    Secure form for Book model with comprehensive validation and sanitization.
    Implements protection against XSS, injection attacks, and data integrity issues.
    """
    
    # Custom validators for enhanced security
    title_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\s\-\.\,\:\;\!\?\'\"\(\)]+$',
        message='Title contains invalid characters. Only letters, numbers, and basic punctuation allowed.',
        code='invalid_title'
    )
    
    author_validator = RegexValidator(
        regex=r'^[a-zA-Z\s\-\.]+$',
        message='Author name can only contain letters, spaces, hyphens, and periods.',
        code='invalid_author'
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': 200,
                'required': True,
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': 100,
                'required': True,
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': 1000,
                'max': 2030,
                'required': True,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add security-focused field configurations
        self.fields['title'].validators.append(self.title_validator)
        self.fields['title'].validators.append(MinLengthValidator(2))
        
        self.fields['author'].validators.append(self.author_validator)
        self.fields['author'].validators.append(MinLengthValidator(2))
        
        # Set help text for security awareness
        self.fields['title'].help_text = 'Enter a valid book title (2-200 characters)'
        self.fields['author'].help_text = 'Enter author name (letters, spaces, hyphens, periods only)'
        self.fields['publication_year'].help_text = 'Enter year between 1000 and 2030'
    
    def clean_title(self):
        """
        Custom validation and sanitization for title field.
        Prevents XSS attacks and ensures data integrity.
        """
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError('Title is required.')
        
        # Strip HTML tags to prevent XSS
        title = strip_tags(title).strip()
        
        # Additional length validation
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
        
        if len(title) > 200:
            raise ValidationError('Title cannot exceed 200 characters.')
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',              # JavaScript protocol
            r'on\w+\s*=',               # Event handlers
            r'<iframe.*?>',             # Iframe tags
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                raise ValidationError('Title contains potentially malicious content.')
        
        return title
    
    def clean_author(self):
        """
        Custom validation and sanitization for author field.
        Ensures only valid author names are accepted.
        """
        author = self.cleaned_data.get('author')
        
        if not author:
            raise ValidationError('Author is required.')
        
        # Strip HTML tags and whitespace
        author = strip_tags(author).strip()
        
        # Length validation
        if len(author) < 2:
            raise ValidationError('Author name must be at least 2 characters long.')
        
        if len(author) > 100:
            raise ValidationError('Author name cannot exceed 100 characters.')
        
        # Check for valid author name format
        if not re.match(r'^[a-zA-Z\s\-\.]+$', author):
            raise ValidationError('Author name contains invalid characters.')
        
        return author
    
    def clean_publication_year(self):
        """
        Custom validation for publication year.
        Ensures realistic year values and prevents injection.
        """
        year = self.cleaned_data.get('publication_year')
        
        if not year:
            raise ValidationError('Publication year is required.')
        
        # Validate year range
        if year < 1000 or year > 2030:
            raise ValidationError('Publication year must be between 1000 and 2030.')
        
        return year
    
    def clean(self):
        """
        Form-level validation for additional security checks.
        Performs cross-field validation and final security checks.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        year = cleaned_data.get('publication_year')
        
        # Cross-field validation
        if title and author:
            # Check for duplicate books (basic business logic)
            existing_book = Book.objects.filter(
                title__iexact=title,
                author__iexact=author,
                publication_year=year
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_book.exists():
                raise ValidationError('A book with this title, author, and year already exists.')
        
        return cleaned_data


class SecureSearchForm(forms.Form):
    """
    Secure search form with input validation and sanitization.
    Protects against SQL injection and XSS attacks in search functionality.
    """
    
    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...',
            'maxlength': 100,
        }),
        help_text='Enter search terms (letters, numbers, and spaces only)'
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('author', 'Author'),
            ('both', 'Title and Author'),
        ],
        initial='both',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select search scope'
    )
    
    def clean_query(self):
        """
        Sanitize and validate search query to prevent injection attacks.
        """
        query = self.cleaned_data.get('query')
        
        if not query:
            raise ValidationError('Search query is required.')
        
        # Strip HTML tags
        query = strip_tags(query).strip()
        
        # Allow only alphanumeric characters, spaces, and basic punctuation
        if not re.match(r'^[a-zA-Z0-9\s\-\.\,\:\;\!\?\'\"\(\)]+$', query):
            raise ValidationError('Search query contains invalid characters.')
        
        # Minimum length check
        if len(query) < 2:
            raise ValidationError('Search query must be at least 2 characters long.')
        
        # Check for SQL injection patterns
        sql_patterns = [
            r'\b(union|select|insert|update|delete|drop|create|alter)\b',
            r'[\'\"]\s*;\s*',
            r'--',
            r'/\*.*?\*/',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                raise ValidationError('Search query contains potentially malicious content.')
        
        return query


class ExampleForm(forms.Form):
    """
    Example form demonstrating Django security best practices.
    This form showcases comprehensive input validation, sanitization,
    and protection against common web vulnerabilities.
    """

    # Text field with comprehensive validation
    name = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'maxlength': 100,
        }),
        help_text='Enter your full name (2-100 characters, letters and spaces only)',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\-\.]+$',
                message='Name can only contain letters, spaces, hyphens, and periods.',
                code='invalid_name'
            )
        ]
    )

    # Email field with built-in validation
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
        }),
        help_text='Enter a valid email address'
    )

    # Choice field for security demonstration
    category = forms.ChoiceField(
        choices=[
            ('general', 'General Inquiry'),
            ('security', 'Security Issue'),
            ('bug', 'Bug Report'),
            ('feature', 'Feature Request'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select the category of your inquiry'
    )

    # Textarea with length validation
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 5,
            'maxlength': 1000,
        }),
        max_length=1000,
        min_length=10,
        required=True,
        help_text='Enter your message (10-1000 characters)'
    )

    # Boolean field for terms acceptance
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='You must accept the terms and conditions'
    )

    def clean_name(self):
        """
        Custom validation and sanitization for name field.
        Demonstrates secure input handling and XSS prevention.
        """
        name = self.cleaned_data.get('name')

        if not name:
            raise ValidationError('Name is required.')

        # Strip HTML tags to prevent XSS
        name = strip_tags(name).strip()

        # Additional length validation
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')

        if len(name) > 100:
            raise ValidationError('Name cannot exceed 100 characters.')

        # Check for valid name format
        if not re.match(r'^[a-zA-Z\s\-\.]+$', name):
            raise ValidationError('Name contains invalid characters.')

        # Check for suspicious patterns (XSS prevention)
        suspicious_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe.*?>',
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, name, re.IGNORECASE):
                raise ValidationError('Name contains potentially malicious content.')

        return name

    def clean_message(self):
        """
        Custom validation and sanitization for message field.
        Ensures message content is safe and appropriate.
        """
        message = self.cleaned_data.get('message')

        if not message:
            raise ValidationError('Message is required.')

        # Strip HTML tags to prevent XSS
        message = strip_tags(message).strip()

        # Length validation
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')

        if len(message) > 1000:
            raise ValidationError('Message cannot exceed 1000 characters.')

        # Check for spam patterns
        spam_patterns = [
            r'\b(viagra|cialis|casino|lottery|winner)\b',
            r'\b(click here|free money|guaranteed)\b',
            r'http[s]?://[^\s]+\.[^\s]+',  # URLs (basic detection)
        ]

        for pattern in spam_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                raise ValidationError('Message contains inappropriate content.')

        # Check for injection patterns
        injection_patterns = [
            r'\b(union|select|insert|update|delete|drop)\b',
            r'[\'\"]\s*;\s*',
            r'--',
            r'/\*.*?\*/',
        ]

        for pattern in injection_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                raise ValidationError('Message contains potentially malicious content.')

        return message

    def clean(self):
        """
        Form-level validation for additional security checks.
        Performs cross-field validation and final security verification.
        """
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        terms_accepted = cleaned_data.get('terms_accepted')

        # Ensure terms are accepted
        if not terms_accepted:
            raise ValidationError('You must accept the terms and conditions to proceed.')

        # Cross-field validation example
        if name and email:
            # Check if name appears to be an email (common mistake)
            if '@' in name:
                raise ValidationError('Please enter your name in the name field, not your email.')

        # Additional security check: ensure message doesn't contain personal info
        if message and email:
            email_parts = email.split('@')
            if len(email_parts) > 1 and email_parts[0].lower() in message.lower():
                self.add_error('message', 'Please avoid including personal information in your message.')

        return cleaned_data
