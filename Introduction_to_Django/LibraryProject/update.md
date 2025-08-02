# Update Operation

## Primary Update Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
```

## Alternative Update Methods
```python
# Using update() method for bulk updates
Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")

# Using get and save for single object
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
```

## Expected Output
```
# No output is displayed, but the book title is successfully updated
```

## Verification
```python
updated_book = Book.objects.get(id=book.id)
print(f"Updated title: {updated_book.title}")
print(f"Author: {updated_book.author}")
print(f"Publication Year: {updated_book.publication_year}")
```

## Expected Verification Output
```
Updated title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```
