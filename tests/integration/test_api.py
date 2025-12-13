"""
Integration tests for API endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from books.models import Book
from loans.models import Loan

User = get_user_model()


class TestAuthenticationAPI:
    """Tests for authentication endpoints."""

    @pytest.mark.django_db
    def test_register_user(self, api_client) -> None:
        """Test user registration."""
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['username'] == 'newuser'

    @pytest.mark.django_db
    def test_register_user_password_mismatch(self, api_client) -> None:
        """Test registration with password mismatch."""
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password2': 'different',
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_login_user(self, api_client, user: User) -> None:
        """Test user login."""
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    @pytest.mark.django_db
    def test_get_current_user(self, authenticated_client, user: User) -> None:
        """Test getting current user info."""
        url = reverse('users:me')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username


class TestBooksAPI:
    """Tests for books endpoints."""

    @pytest.mark.django_db
    def test_list_books_anonymous(self, api_client, book: Book) -> None:
        """Test listing books as anonymous user."""
        url = reverse('books:book-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    @pytest.mark.django_db
    def test_list_books_filtered(self, api_client, book: Book) -> None:
        """Test filtering books."""
        Book.objects.create(
            title='Another Book',
            author='Another Author',
            isbn='9876543210',
            page_count=200,
        )
        url = reverse('books:book-list')
        response = api_client.get(url, {'author': 'Test Author'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    @pytest.mark.django_db
    def test_search_books(self, api_client, book: Book) -> None:
        """Test searching books."""
        url = reverse('books:book-list')
        response = api_client.get(url, {'search': 'Test'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    @pytest.mark.django_db
    def test_get_book_detail(self, api_client, book: Book) -> None:
        """Test getting book details."""
        url = reverse('books:book-detail', kwargs={'pk': book.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == book.title

    @pytest.mark.django_db
    def test_create_book_anonymous(self, api_client) -> None:
        """Test creating book as anonymous user (should fail)."""
        url = reverse('books:book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '1111111111',
            'page_count': 150,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_book_regular_user(self, authenticated_client) -> None:
        """Test creating book as regular user (should fail)."""
        url = reverse('books:book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '1111111111',
            'page_count': 150,
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_book_admin(self, admin_client) -> None:
        """Test creating book as admin."""
        url = reverse('books:book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '1111111111',
            'page_count': 150,
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Book'

    @pytest.mark.django_db
    def test_update_book_admin(self, admin_client, book: Book) -> None:
        """Test updating book as admin."""
        url = reverse('books:book-detail', kwargs={'pk': book.id})
        data = {
            'title': 'Updated Book',
            'author': book.author,
            'isbn': book.isbn,
            'page_count': book.page_count,
        }
        response = admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Book'

    @pytest.mark.django_db
    def test_delete_book_admin(self, admin_client, book: Book) -> None:
        """Test deleting book as admin."""
        url = reverse('books:book-detail', kwargs={'pk': book.id})
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.filter(id=book.id).exists() is False


class TestBorrowReturnAPI:
    """Tests for borrow/return endpoints."""

    @pytest.mark.django_db
    def test_borrow_book_success(self, authenticated_client, book: Book, user: User) -> None:
        """Test borrowing a book."""
        url = reverse('books:book-borrow', kwargs={'pk': book.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'loan_id' in response.data
        # Check book is now unavailable
        book.refresh_from_db()
        assert book.is_available is False
        # Check loan was created
        assert Loan.objects.filter(user=user, book=book, returned_at__isnull=True).exists() is True

    @pytest.mark.django_db
    def test_borrow_book_anonymous(self, api_client, book: Book) -> None:
        """Test borrowing as anonymous user (should fail)."""
        url = reverse('books:book-borrow', kwargs={'pk': book.id})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_borrow_unavailable_book(self, authenticated_client, unavailable_book: Book) -> None:
        """Test borrowing an unavailable book."""
        url = reverse('books:book-borrow', kwargs={'pk': unavailable_book.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_borrow_same_book_twice(self, authenticated_client, book: Book, user: User) -> None:
        """Test borrowing the same book twice."""
        url = reverse('books:book-borrow', kwargs={'pk': book.id})
        authenticated_client.post(url)
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_return_book_success(self, authenticated_client, book: Book, user: User) -> None:
        """Test returning a book."""
        # First borrow
        borrow_url = reverse('books:book-borrow', kwargs={'pk': book.id})
        authenticated_client.post(borrow_url)
        # Then return
        return_url = reverse('books:book-return_book', kwargs={'pk': book.id})
        response = authenticated_client.post(return_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'returned_at' in response.data
        # Check book is now available
        book.refresh_from_db()
        assert book.is_available is True
        # Check loan was marked as returned
        loan = Loan.objects.get(user=user, book=book)
        assert loan.returned_at is not None

    @pytest.mark.django_db
    def test_return_book_without_loan(self, authenticated_client, book: Book) -> None:
        """Test returning a book without borrowing it."""
        url = reverse('books:book-return_book', kwargs={'pk': book.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestLoansAPI:
    """Tests for loans endpoints."""

    @pytest.mark.django_db
    def test_list_loans(self, authenticated_client, user: User, book: Book) -> None:
        """Test listing user's loans."""
        Loan.objects.create(user=user, book=book)
        url = reverse('loans:loan-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Response is paginated, so check results
        assert len(response.data['results']) == 1

    def test_list_loans_anonymous(self, api_client) -> None:
        """Test listing loans as anonymous user (should fail)."""
        url = reverse('loans:loan-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestEndToEndFlow:
    """End-to-end integration tests."""

    @pytest.mark.django_db
    def test_complete_borrow_return_flow(
        self, authenticated_client, book: Book, user: User
    ) -> None:
        """Test complete borrow -> return flow."""
        # Initial state: book is available
        assert book.is_available is True
        assert Loan.objects.filter(user=user, book=book).count() == 0

        # Borrow the book
        borrow_url = reverse('books:book-borrow', kwargs={'pk': book.id})
        borrow_response = authenticated_client.post(borrow_url)
        assert borrow_response.status_code == status.HTTP_201_CREATED

        # Verify book is unavailable
        book.refresh_from_db()
        assert book.is_available is False

        # Verify loan exists and is active
        loan = Loan.objects.get(user=user, book=book)
        assert loan.returned_at is None

        # Return the book
        return_url = reverse('books:book-return_book', kwargs={'pk': book.id})
        return_response = authenticated_client.post(return_url)
        assert return_response.status_code == status.HTTP_200_OK

        # Verify book is available again
        book.refresh_from_db()
        assert book.is_available is True

        # Verify loan is marked as returned
        loan.refresh_from_db()
        assert loan.returned_at is not None

        # Verify loan appears in user's loan list
        loans_url = reverse('loans:loan-list')
        loans_response = authenticated_client.get(loans_url)
        assert loans_response.status_code == status.HTTP_200_OK
        # Response is paginated, so check results
        assert len(loans_response.data['results']) == 1
        assert loans_response.data['results'][0]['is_active'] is False
