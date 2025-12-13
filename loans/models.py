"""
Loan models for the Library Management System.
"""
from django.contrib.auth import get_user_model
from django.db import models

from books.models import Book

User = get_user_model()


class Loan(models.Model):
    """
    Loan model representing a book loan transaction.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'loans'
        ordering = ['-borrowed_at']
        indexes = [
            models.Index(fields=['user', 'returned_at']),
            models.Index(fields=['book', 'returned_at']),
        ]

    def __str__(self) -> str:
        status = 'returned' if self.returned_at else 'borrowed'
        return f'{self.user.username} - {self.book.title} ({status})'

    @property
    def is_active(self) -> bool:
        """Check if the loan is currently active."""
        return self.returned_at is None
