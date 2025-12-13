"""
Filters for Book model.
"""
import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    """Filter set for Book model."""

    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    isbn = django_filters.CharFilter(lookup_expr='exact')
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = Book
        fields = ('title', 'author', 'isbn', 'is_available')
