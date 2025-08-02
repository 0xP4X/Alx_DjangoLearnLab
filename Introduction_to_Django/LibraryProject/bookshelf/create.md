# Create Operation

## Method 1: Using Constructor and Save
```python
from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
```

## Method 2: Using Book.objects.create()
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output
```
# The book instance is created and saved to the database
# No output is displayed, but the book is successfully created with ID assigned
```

## Verification
```python
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
print(f"Book ID: {book.id}")
```

## Expected Verification Output
```
Book created: 1984 by George Orwell (1949)
Book ID: 1
```
