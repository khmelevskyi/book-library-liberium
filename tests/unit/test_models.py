"""
Unit tests for models.
"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError

import pytest

from books.models import Book
from loans.models import Loan

User = get_user_model()


class TestBookModel:
    """Tests for Book model."""

    @pytest.mark.django_db
    def test_create_book(self) -> None:
        """Test creating a book."""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            page_count=100,
        )
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.isbn == "1234567890"
        assert book.page_count == 100
        assert book.is_available is True
        assert book.id is not None

    @pytest.mark.django_db
    def test_book_str(self) -> None:
        """Test Book __str__ method."""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            page_count=100,
        )
        assert str(book) == "Test Book by Test Author"

    @pytest.mark.django_db
    def test_book_unique_isbn(self) -> None:
        """Test that ISBN must be unique."""
        Book.objects.create(
            title="Book 1",
            author="Author",
            isbn="1234567890",
            page_count=100,
        )
        with pytest.raises(IntegrityError):
            Book.objects.create(
                title="Book 2",
                author="Author",
                isbn="1234567890",
                page_count=200,
            )


class TestLoanModel:
    """Tests for Loan model."""

    @pytest.mark.django_db
    def test_create_loan(self, user: User, book: Book) -> None:
        """Test creating a loan."""
        loan = Loan.objects.create(user=user, book=book)
        assert loan.user == user
        assert loan.book == book
        assert loan.borrowed_at is not None
        assert loan.returned_at is None
        assert loan.is_active is True

    @pytest.mark.django_db
    def test_loan_str_active(self, user: User, book: Book) -> None:
        """Test Loan __str__ method for active loan."""
        loan = Loan.objects.create(user=user, book=book)
        assert "borrowed" in str(loan).lower()

    @pytest.mark.django_db
    def test_loan_str_returned(self, user: User, book: Book) -> None:
        """Test Loan __str__ method for returned loan."""
        from django.utils import timezone

        loan = Loan.objects.create(user=user, book=book)
        loan.returned_at = timezone.now()
        loan.save()
        assert "returned" in str(loan).lower()
        assert loan.is_active is False

    @pytest.mark.django_db
    def test_loan_is_active_property(self, user: User, book: Book) -> None:
        """Test Loan is_active property."""
        loan = Loan.objects.create(user=user, book=book)
        assert loan.is_active is True

        from django.utils import timezone

        loan.returned_at = timezone.now()
        loan.save()
        assert loan.is_active is False
