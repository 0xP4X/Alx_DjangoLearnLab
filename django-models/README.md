# Django Models - Complex Relationships Project

## Objective
Master Django's ORM capabilities by creating models that demonstrate ForeignKey, ManyToMany, and OneToOne relationships.

## Project Structure
```
django-models/
└── LibraryProject/
    ├── relationship_app/
    │   ├── models.py          # Complex relationship models
    │   ├── query_samples.py   # Sample queries demonstrating relationships
    │   └── migrations/        # Database migration files
    ├── bookshelf/             # Previous bookshelf app
    └── manage.py
```

## Models Implemented

### 1. Author Model
- **Field**: `name` (CharField)
- **Relationship**: One-to-Many with Book (ForeignKey)

### 2. Book Model  
- **Fields**: `title` (CharField), `author` (ForeignKey)
- **Relationship**: Many-to-One with Author, Many-to-Many with Library

### 3. Library Model
- **Fields**: `name` (CharField), `books` (ManyToManyField)
- **Relationship**: Many-to-Many with Book, One-to-One with Librarian

### 4. Librarian Model
- **Fields**: `name` (CharField), `library` (OneToOneField)
- **Relationship**: One-to-One with Library

## Relationship Types Demonstrated

### ForeignKey (One-to-Many)
- **Book → Author**: Each book has one author, but an author can have multiple books
- **Implementation**: `author = models.ForeignKey(Author, on_delete=models.CASCADE)`

### ManyToManyField (Many-to-Many)
- **Library ↔ Book**: A library can have multiple books, and a book can be in multiple libraries
- **Implementation**: `books = models.ManyToManyField(Book)`

### OneToOneField (One-to-One)
- **Librarian → Library**: Each librarian manages exactly one library
- **Implementation**: `library = models.OneToOneField(Library, on_delete=models.CASCADE)`

## Sample Queries

The `query_samples.py` file contains three main query functions:

### 1. Query Books by Author (ForeignKey)
```python
def query_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books
```

### 2. List Books in Library (ManyToMany)
```python
def list_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books
```

### 3. Retrieve Librarian for Library (OneToOne)
```python
def retrieve_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    return librarian
```

## Setup Instructions

1. **Navigate to project directory**:
   ```bash
   cd django-models/LibraryProject
   ```

2. **Apply migrations**:
   ```bash
   python manage.py makemigrations relationship_app
   python manage.py migrate
   ```

3. **Run sample queries**:
   ```bash
   python manage.py shell
   >>> exec(open('relationship_app/query_samples.py').read())
   ```

## Database Schema

```
Author (1) ←→ (Many) Book (Many) ←→ (Many) Library (1) ←→ (1) Librarian
```

- **Author** has many **Books** (ForeignKey)
- **Library** has many **Books** and vice versa (ManyToMany)  
- **Library** has one **Librarian** (OneToOne)

## Key Features

✅ **ForeignKey Relationship**: Book → Author  
✅ **ManyToMany Relationship**: Library ↔ Book  
✅ **OneToOne Relationship**: Librarian → Library  
✅ **Sample Data Creation**: Automated test data generation  
✅ **Query Demonstrations**: Practical examples of each relationship type  
✅ **Proper Model Methods**: `__str__` methods for better representation  

## Testing

The models have been tested with sample data creation and all relationship queries work correctly:

- Authors can have multiple books
- Libraries can contain multiple books
- Books can be in multiple libraries  
- Each library has exactly one librarian

This project demonstrates mastery of Django's ORM relationship capabilities and provides a solid foundation for complex database modeling.
