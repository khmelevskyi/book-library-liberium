from django.contrib import admin

from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Admin configuration for Loan model."""
    list_display = ('user', 'book', 'borrowed_at', 'returned_at', 'is_active')
    list_filter = ('borrowed_at', 'returned_at')
    search_fields = ('user__username', 'book__title', 'book__author')
    readonly_fields = ('borrowed_at',)
    date_hierarchy = 'borrowed_at'
