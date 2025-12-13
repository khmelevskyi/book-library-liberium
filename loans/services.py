"""
Business logic services for Loan operations.
"""
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from books.models import Book

from .models import Loan

User = get_user_model()


class LoanService:
    """Service class for loan-related business logic."""

    @staticmethod
    @transaction.atomic
    def borrow_book(user: User, book: Book) -> Loan:
        """
        Borrow a book for a user.

        Args:
            user: The user borrowing the book
            book: The book to borrow

        Returns:
            Loan instance

        Raises:
            ValueError: If book is unavailable or user already has an active loan for this book
        """
        # Check if user already has an active loan for this book
        active_loan = Loan.objects.filter(user=user, book=book, returned_at__isnull=True).first()
        if active_loan:
            raise ValueError(f'You already have an active loan for "{book.title}".'
                             'Please return it first.')

        # Check if book is available
        if not book.is_available:
            raise ValueError(f'Book "{book.title}" is not available for borrowing.')

        # Create loan and mark book as unavailable
        loan = Loan.objects.create(user=user, book=book)
        book.is_available = False
        book.save(update_fields=['is_available'])

        return loan

    @staticmethod
    @transaction.atomic
    def return_book(user: User, book: Book) -> Loan:
        """
        Return a book for a user.

        Args:
            user: The user returning the book
            book: The book to return

        Returns:
            Loan instance

        Raises:
            ValueError: If user doesn't have an active loan for this book
        """
        # Find active loan
        loan = Loan.objects.filter(user=user, book=book, returned_at__isnull=True).first()
        if not loan:
            raise ValueError(f'You do not have an active loan for "{book.title}".')

        # Mark loan as returned and make book available
        loan.returned_at = timezone.now()
        loan.save(update_fields=['returned_at'])

        book.is_available = True
        book.save(update_fields=['is_available'])

        return loan
