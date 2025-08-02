# Delete Operation

## Primary Delete Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
```

## Alternative Delete Methods
```python
# Delete using filter (bulk delete)
Book.objects.filter(title="Nineteen Eighty-Four").delete()

# Delete by ID
Book.objects.get(id=1).delete()
```

## Expected Output
```
(1, {'bookshelf.Book': 1})
```

## Verification
```python
# Try to retrieve all books to confirm deletion
all_books = Book.objects.all()
print(f"Number of books: {all_books.count()}")
print(f"Books: {all_books}")
```

## Expected Verification Output
```
Number of books: 0
Books: <QuerySet []>
```

## Alternative Verification
```python
# Try to retrieve the deleted book (should raise DoesNotExist exception)
try:
    deleted_book = Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists")
except Book.DoesNotExist:
    print("Book successfully deleted - DoesNotExist exception raised")
```

## Expected Alternative Verification Output
```
Book successfully deleted - DoesNotExist exception raised
```
