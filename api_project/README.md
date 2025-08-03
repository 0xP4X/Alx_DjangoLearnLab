# Django REST Framework API Project

## Overview
This is a Django project specifically designed for building APIs using Django REST Framework (DRF). The project demonstrates the initial setup and configuration necessary to create robust API endpoints.

## Project Structure
```
api_project/
├── api_project/           # Main project directory
│   ├── __init__.py
│   ├── settings.py        # Project settings with DRF configuration
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── api/                  # API app for handling API logic
│   ├── __init__.py
│   ├── models.py         # Book model for API demonstration
│   ├── admin.py          # Admin configuration
│   ├── apps.py           # App configuration
│   ├── views.py          # API views
│   ├── tests.py          # Test cases
│   └── migrations/       # Database migrations
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Setup Instructions

### Step 1: Install Dependencies
```bash
# Install Django and Django REST Framework
pip install -r requirements.txt

# Or install individually:
pip install Django>=4.2.0
pip install djangorestframework>=3.14.0
```

### Step 2: Database Setup
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser (Optional)
```bash
# Create an admin user for Django admin interface
python manage.py createsuperuser
```

### Step 4: Start Development Server
```bash
# Start the Django development server
python manage.py runserver

# Or specify a custom port
python manage.py runserver 8001
```

### Step 5: Enable Django REST Framework
After installing djangorestframework, uncomment the following line in `api_project/settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',  # Uncomment this line
    'api',
]
```

## Models

### Book Model
The project includes a simple `Book` model for API demonstration:

```python
class Book(models.Model):
    title = models.CharField(max_length=200, help_text="The title of the book")
    author = models.CharField(max_length=100, help_text="The author of the book")
    
    def __str__(self):
        return f"{self.title} by {self.author}"
```

## Django REST Framework Configuration

The project is pre-configured with Django REST Framework settings in `settings.py`:

- **Authentication**: Session and Basic authentication
- **Permissions**: Authenticated users by default
- **Pagination**: Page number pagination with 20 items per page
- **Throttling**: Rate limiting for anonymous and authenticated users
- **API Versioning**: Accept header versioning

## API Endpoints (Future Implementation)

Once Django REST Framework is fully integrated, the following endpoints will be available:

- `GET /api/books/` - List all books
- `POST /api/books/` - Create a new book
- `GET /api/books/{id}/` - Retrieve a specific book
- `PUT /api/books/{id}/` - Update a specific book
- `DELETE /api/books/{id}/` - Delete a specific book

## Development Workflow

1. **Model Development**: Define your data models in `api/models.py`
2. **Serializer Creation**: Create DRF serializers for your models
3. **View Implementation**: Implement API views using DRF ViewSets or APIViews
4. **URL Configuration**: Configure URL routing for your API endpoints
5. **Testing**: Write comprehensive tests for your API endpoints

## Testing

Run the test suite with:
```bash
python manage.py test
```

## Admin Interface

Access the Django admin interface at:
- URL: `http://127.0.0.1:8000/admin/` (or your custom port)
- Use the superuser credentials created in Step 3

## Next Steps

1. Install Django REST Framework: `pip install djangorestframework`
2. Uncomment `'rest_framework'` in `INSTALLED_APPS`
3. Create serializers for the Book model
4. Implement API views and viewsets
5. Configure URL routing for API endpoints
6. Add authentication and permissions as needed
7. Write comprehensive tests for your API

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'rest_framework'**
   - Solution: Install Django REST Framework with `pip install djangorestframework`

2. **Server not starting**
   - Check for syntax errors in your code
   - Ensure all migrations are applied: `python manage.py migrate`
   - Verify INSTALLED_APPS configuration in settings.py

3. **Database errors**
   - Run migrations: `python manage.py makemigrations` then `python manage.py migrate`
   - Check database configuration in settings.py

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)

## License

This project is for educational purposes as part of the ALX Django Learning Lab.
