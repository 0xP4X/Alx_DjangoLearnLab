"""
Django REST Framework Serializers for the API app.
This module will contain serializers for converting model instances to JSON and vice versa.

Note: This file is prepared for Django REST Framework integration.
Uncomment and modify the code below after installing djangorestframework.
"""

# from rest_framework import serializers
# from .models import Book


# class BookSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Book model.
#     Handles serialization and deserialization of Book instances for API responses.
#     """
#     
#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'author']
#         read_only_fields = ['id']
#     
#     def validate_title(self, value):
#         """
#         Custom validation for the title field.
#         Ensures the title is not empty and has a reasonable length.
#         """
#         if not value or len(value.strip()) == 0:
#             raise serializers.ValidationError("Title cannot be empty.")
#         
#         if len(value) > 200:
#             raise serializers.ValidationError("Title cannot exceed 200 characters.")
#         
#         return value.strip()
#     
#     def validate_author(self, value):
#         """
#         Custom validation for the author field.
#         Ensures the author name is not empty and has a reasonable length.
#         """
#         if not value or len(value.strip()) == 0:
#             raise serializers.ValidationError("Author cannot be empty.")
#         
#         if len(value) > 100:
#             raise serializers.ValidationError("Author name cannot exceed 100 characters.")
#         
#         return value.strip()
#     
#     def validate(self, data):
#         """
#         Object-level validation.
#         Ensures that the combination of title and author is unique.
#         """
#         title = data.get('title')
#         author = data.get('author')
#         
#         if title and author:
#             # Check if a book with the same title and author already exists
#             existing_book = Book.objects.filter(
#                 title__iexact=title,
#                 author__iexact=author
#             ).exclude(pk=self.instance.pk if self.instance else None)
#             
#             if existing_book.exists():
#                 raise serializers.ValidationError(
#                     "A book with this title and author already exists."
#                 )
#         
#         return data


# Additional serializers can be added here for other models:

# class AuthorSerializer(serializers.ModelSerializer):
#     """
#     Serializer for Author model (if implemented in the future).
#     """
#     books = BookSerializer(many=True, read_only=True)
#     
#     class Meta:
#         model = Author
#         fields = ['id', 'name', 'bio', 'books']

# class BookDetailSerializer(BookSerializer):
#     """
#     Extended serializer for detailed book information.
#     Includes additional fields for detailed views.
#     """
#     
#     class Meta(BookSerializer.Meta):
#         fields = BookSerializer.Meta.fields + ['created_at', 'updated_at']
