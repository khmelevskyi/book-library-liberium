"""
Book models for the Library Management System.
"""

from django.core.validators import MinLengthValidator
from django.db import models


class Book(models.Model):
    """
    Book model representing a book in the library.
    """

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(
        max_length=13,
        unique=True,
        validators=[MinLengthValidator(10)],
        help_text="ISBN-10 or ISBN-13",
    )
    page_count = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "books"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["isbn"]),
            models.Index(fields=["is_available"]),
            models.Index(fields=["title", "author"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
