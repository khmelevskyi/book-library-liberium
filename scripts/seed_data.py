"""
Script to seed the database with sample data.
"""

import os
import sys

import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

# Django models must be imported after django.setup()
from books.models import Book  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()


def seed_books() -> None:
    """Seed sample books."""
    books_data = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "9780743273565",
            "page_count": 180,
            "is_available": True,
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "9780061120084",
            "page_count": 376,
            "is_available": True,
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "9780451524935",
            "page_count": 328,
            "is_available": True,
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "isbn": "9780141439518",
            "page_count": 432,
            "is_available": True,
        },
        {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "isbn": "9780316769488",
            "page_count": 277,
            "is_available": True,
        },
    ]

    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            isbn=book_data["isbn"],
            defaults=book_data,
        )
        if created:
            print(f"Created book: {book.title}")
        else:
            print(f"Book already exists: {book.title}")


def seed_users() -> None:
    """Seed sample users."""
    users_data = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "password": "testpass123",
            "first_name": "Jane",
            "last_name": "Smith",
        },
    ]

    for user_data in users_data:
        password = user_data.pop("password")
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults=user_data,
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")


if __name__ == "__main__":
    print("Seeding database...")
    seed_books()
    seed_users()
    print("Done!")
