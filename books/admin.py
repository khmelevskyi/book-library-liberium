from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""

    list_display = ("title", "author", "isbn", "page_count", "is_available", "created_at")
    list_filter = ("is_available", "created_at")
    search_fields = ("title", "author", "isbn")
    readonly_fields = ("created_at", "updated_at")
