"""
Serializers for Book model.
"""
import re

from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model."""

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'page_count',
                  'is_available', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_isbn(self, value: str) -> str:
        """Validate ISBN format (10 or 13 digits, with optional hyphens)."""
        # Remove hyphens and spaces
        isbn_clean = re.sub(r'[-\s]', '', value)
        # Check if it's 10 or 13 digits
        if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
            raise serializers.ValidationError('ISBN must be 10 or 13 digits long.')
        # Check if all characters are digits (or X for ISBN-10)
        if not re.match(r'^[\dX]+$', isbn_clean):
            raise serializers.ValidationError('ISBN must contain only digits (or X for ISBN-10).')
        return isbn_clean

    def validate_page_count(self, value: int) -> int:
        """Validate page count is positive."""
        if value <= 0:
            raise serializers.ValidationError('Page count must be greater than 0.')
        return value
