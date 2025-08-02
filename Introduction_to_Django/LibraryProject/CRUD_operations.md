# CRUD Operations Documentation

This document contains all the CRUD operations performed on the Book model in the Django shell.

## Setup
First, start the Django shell:
```bash
python manage.py shell
```

## 1. CREATE Operation

### Import the model
```python
from bookshelf.models import Book
```

### Create a new book instance
```python
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
```

### Verify creation
```python
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
print(f"Book ID: {book.id}")
```

**Expected Output:**
```
Book created: 1984 by George Orwell (1949)
Book ID: 1
```

## 2. RETRIEVE Operation

### Retrieve the book by title
```python
retrieved_book = Book.objects.get(title="1984")
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Publication Year: {retrieved_book.publication_year}")
print(f"ID: {retrieved_book.id}")
```

**Expected Output:**
```
Title: 1984
Author: George Orwell
Publication Year: 1949
ID: 1
```

### Alternative: Retrieve all books
```python
all_books = Book.objects.all()
print(f"All books: {all_books}")
for book in all_books:
    print(f"- {book.title} by {book.author}")
```

**Expected Output:**
```
All books: <QuerySet [<Book: 1984>]>
- 1984 by George Orwell
```

## 3. UPDATE Operation

### Update the book title
```python
book.title = "Nineteen Eighty-Four"
book.save()
```

### Verify the update
```python
updated_book = Book.objects.get(id=book.id)
print(f"Updated title: {updated_book.title}")
print(f"Author: {updated_book.author}")
print(f"Publication Year: {updated_book.publication_year}")
```

**Expected Output:**
```
Updated title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```

## 4. DELETE Operation

### Delete the book
```python
delete_result = book.delete()
print(f"Delete result: {delete_result}")
```

**Expected Output:**
```
Delete result: (1, {'bookshelf.Book': 1})
```

### Verify deletion
```python
all_books = Book.objects.all()
print(f"Number of books after deletion: {all_books.count()}")
print(f"Books: {all_books}")
```

**Expected Output:**
```
Number of books after deletion: 0
Books: <QuerySet []>
```

### Alternative verification - try to retrieve deleted book
```python
try:
    deleted_book = Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists")
except Book.DoesNotExist:
    print("Book successfully deleted - DoesNotExist exception raised")
```

**Expected Output:**
```
Book successfully deleted - DoesNotExist exception raised
```

## Summary

All CRUD operations have been successfully demonstrated:
- **CREATE**: Created a Book instance with title "1984", author "George Orwell", and publication year 1949
- **RETRIEVE**: Retrieved the book by title and displayed all its attributes
- **UPDATE**: Updated the book title from "1984" to "Nineteen Eighty-Four"
- **DELETE**: Deleted the book and confirmed the deletion

The Book model is working correctly with all basic database operations.
