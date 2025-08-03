"""
Sample queries demonstrating Django ORM relationships
This script contains queries for ForeignKey, ManyToMany, and OneToOne relationships

To run this script, use Django shell:
python manage.py shell
>>> exec(open('relationship_app/query_samples.py').read())
"""

# Import models (Django environment should already be set up when using shell)
from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author using ForeignKey relationship
    """
    try:
        # Get the author object
        author = Author.objects.get(name=author_name)
        
        # Query all books by this author using the ForeignKey relationship
        books = Book.objects.filter(author=author)
        
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        
        return books
    
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None


def list_books_in_library(library_name):
    """
    List all books in a library using ManyToMany relationship
    """
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Query all books in this library using the ManyToMany relationship
        books = library.books.all()
        
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        
        return books
    
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library using OneToOne relationship
    """
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Query the librarian for this library using the OneToOne relationship
        librarian = Librarian.objects.get(library=library)
        
        print(f"Librarian for {library_name}: {librarian.name}")
        
        return librarian
    
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'.")
        return None


def create_sample_data():
    """
    Create sample data for testing the queries
    """
    print("Creating sample data...")
    
    # Create authors
    author1, created = Author.objects.get_or_create(name="George Orwell")
    author2, created = Author.objects.get_or_create(name="Jane Austen")
    author3, created = Author.objects.get_or_create(name="Mark Twain")
    
    # Create books
    book1, created = Book.objects.get_or_create(title="1984", author=author1)
    book2, created = Book.objects.get_or_create(title="Animal Farm", author=author1)
    book3, created = Book.objects.get_or_create(title="Pride and Prejudice", author=author2)
    book4, created = Book.objects.get_or_create(title="Emma", author=author2)
    book5, created = Book.objects.get_or_create(title="The Adventures of Tom Sawyer", author=author3)
    
    # Create libraries
    library1, created = Library.objects.get_or_create(name="Central Library")
    library2, created = Library.objects.get_or_create(name="Community Library")
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    
    # Create librarians
    librarian1, created = Librarian.objects.get_or_create(name="Alice Johnson", library=library1)
    librarian2, created = Librarian.objects.get_or_create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!")


def run_sample_queries():
    """
    Run all sample queries to demonstrate the relationships
    """
    print("=" * 50)
    print("DJANGO ORM RELATIONSHIP QUERIES DEMONSTRATION")
    print("=" * 50)
    
    # Create sample data first
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("1. FOREIGNKEY RELATIONSHIP - Books by Author")
    print("=" * 50)
    query_books_by_author("George Orwell")
    print()
    query_books_by_author("Jane Austen")
    
    print("\n" + "=" * 50)
    print("2. MANYTOMANY RELATIONSHIP - Books in Library")
    print("=" * 50)
    list_books_in_library("Central Library")
    print()
    list_books_in_library("Community Library")
    
    print("\n" + "=" * 50)
    print("3. ONETOONE RELATIONSHIP - Librarian for Library")
    print("=" * 50)
    retrieve_librarian_for_library("Central Library")
    print()
    retrieve_librarian_for_library("Community Library")
    
    print("\n" + "=" * 50)
    print("QUERIES COMPLETED SUCCESSFULLY!")
    print("=" * 50)


if __name__ == "__main__":
    run_sample_queries()
