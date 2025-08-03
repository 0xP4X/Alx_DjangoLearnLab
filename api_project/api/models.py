from django.db import models


class Book(models.Model):
    """
    Simple Book model for API demonstration.
    This model represents a book with basic information.
    """
    title = models.CharField(
        max_length=200,
        help_text="The title of the book"
    )
    author = models.CharField(
        max_length=100,
        help_text="The author of the book"
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"
