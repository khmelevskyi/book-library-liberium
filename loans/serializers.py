"""
Serializers for Loan model.
"""
from rest_framework import serializers

from books.serializers import BookSerializer
from users.serializers import UserSerializer

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model."""
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ('id', 'user', 'book', 'borrowed_at', 'returned_at', 'is_active')
        read_only_fields = ('id', 'borrowed_at', 'returned_at', 'is_active')
