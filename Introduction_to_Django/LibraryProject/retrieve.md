# Retrieve Operation

## Primary Retrieve Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"ID: {book.id}")
```

## Expected Output
```
Title: 1984
Author: George Orwell
Publication Year: 1949
ID: 1
```

## Alternative Retrieval Methods
```python
# Retrieve all books
all_books = Book.objects.all()
print(all_books)

# Retrieve by ID
book_by_id = Book.objects.get(id=1)
print(book_by_id)

# Retrieve using filter
books = Book.objects.filter(author="George Orwell")
print(books)
```

## Expected Alternative Output
```
<QuerySet [<Book: 1984>]>
<Book: 1984>
<QuerySet [<Book: 1984>]>
```
