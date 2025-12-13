"""
Unit tests for services.
"""
import pytest
from django.contrib.auth import get_user_model

from books.models import Book
from loans.services import LoanService

User = get_user_model()


class TestLoanService:
    """Tests for LoanService."""

    @pytest.mark.django_db
    def test_borrow_book_success(self, user: User, book: Book) -> None:
        """Test successful book borrowing."""
        assert book.is_available is True
        loan = LoanService.borrow_book(user=user, book=book)
        assert loan.user == user
        assert loan.book == book
        assert loan.returned_at is None
        # Book should be marked as unavailable
        book.refresh_from_db()
        assert book.is_available is False

    @pytest.mark.django_db
    def test_borrow_unavailable_book(self, user: User, unavailable_book: Book) -> None:
        """Test borrowing an unavailable book."""
        with pytest.raises(ValueError, match='not available'):
            LoanService.borrow_book(user=user, book=unavailable_book)

    @pytest.mark.django_db
    def test_borrow_same_book_twice(self, user: User, book: Book) -> None:
        """Test borrowing the same book twice."""
        LoanService.borrow_book(user=user, book=book)
        with pytest.raises(ValueError, match='already have an active loan'):
            LoanService.borrow_book(user=user, book=book)

    @pytest.mark.django_db
    def test_return_book_success(self, user: User, book: Book) -> None:
        """Test successful book return."""
        loan = LoanService.borrow_book(user=user, book=book)
        assert book.is_available is False

        returned_loan = LoanService.return_book(user=user, book=book)
        assert returned_loan.id == loan.id
        assert returned_loan.returned_at is not None
        # Book should be marked as available
        book.refresh_from_db()
        assert book.is_available is True

    @pytest.mark.django_db
    def test_return_book_without_loan(self, user: User, book: Book) -> None:
        """Test returning a book without an active loan."""
        with pytest.raises(ValueError, match='do not have an active loan'):
            LoanService.return_book(user=user, book=book)

    @pytest.mark.django_db
    def test_return_already_returned_book(self, user: User, book: Book) -> None:
        """Test returning a book that was already returned."""
        LoanService.borrow_book(user=user, book=book)
        LoanService.return_book(user=user, book=book)
        with pytest.raises(ValueError, match='do not have an active loan'):
            LoanService.return_book(user=user, book=book)
