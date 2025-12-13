"""
Pytest configuration and fixtures.
"""

from django.contrib.auth import get_user_model

import pytest
from rest_framework.test import APIClient

from books.models import Book

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """Create an API client."""
    return APIClient()


@pytest.fixture
def user() -> User:
    """Create a regular user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def admin_user() -> User:
    """Create an admin user."""
    return User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def authenticated_client(api_client: APIClient, user: User) -> APIClient:
    """Create an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client: APIClient, admin_user: User) -> APIClient:
    """Create an authenticated admin API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def book() -> Book:
    """Create a book."""
    return Book.objects.create(
        title="Test Book",
        author="Test Author",
        isbn="1234567890",
        page_count=100,
        is_available=True,
    )


@pytest.fixture
def unavailable_book() -> Book:
    """Create an unavailable book."""
    return Book.objects.create(
        title="Unavailable Book",
        author="Test Author",
        isbn="0987654321",
        page_count=200,
        is_available=False,
    )
