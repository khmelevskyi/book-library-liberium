"""
Unit tests for serializers.
"""
import pytest

from books.serializers import BookSerializer
from users.serializers import RegisterSerializer


class TestBookSerializer:
    """Tests for BookSerializer."""

    @pytest.mark.django_db
    def test_valid_book_data(self) -> None:
        """Test serializer with valid data."""
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'page_count': 100,
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_invalid_isbn_length(self) -> None:
        """Test ISBN validation - too short."""
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '12345',
            'page_count': 100,
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'isbn' in serializer.errors

    @pytest.mark.django_db
    def test_invalid_isbn_characters(self) -> None:
        """Test ISBN validation - invalid characters."""
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '12345-67890-abc',
            'page_count': 100,
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'isbn' in serializer.errors

    @pytest.mark.django_db
    def test_valid_isbn_13(self) -> None:
        """Test ISBN-13 validation."""
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '9781234567890',
            'page_count': 100,
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_invalid_page_count_zero(self) -> None:
        """Test page count validation - zero."""
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'page_count': 0,
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'page_count' in serializer.errors

    @pytest.mark.django_db
    def test_invalid_page_count_negative(self) -> None:
        """Test page count validation - negative."""
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'page_count': -10,
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'page_count' in serializer.errors


class TestRegisterSerializer:
    """Tests for RegisterSerializer."""

    @pytest.mark.django_db
    def test_valid_registration(self) -> None:
        """Test serializer with valid data."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_password_mismatch(self) -> None:
        """Test password mismatch validation."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'differentpass',
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'password' in serializer.errors

    @pytest.mark.django_db
    def test_create_user(self) -> None:
        """Test user creation."""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid() is True
        user = serializer.save()
        assert user.username == 'newuser'
        assert user.email == 'new@example.com'
        assert user.check_password('newpass123') is True
